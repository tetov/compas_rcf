"""Fabrication runner placing elements according to fab_data and conf."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import logging
import re
import threading
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler
from queue import Queue

import compas_rrc
import confuse
import questionary
from compas.utilities import DataEncoder

from rapid_clay_formations_fab.fab_data import PlaceElement
from rapid_clay_formations_fab.robots import AbbRcfFabricationClient
from rapid_clay_formations_fab.robots import PrintTextNoErase
from rapid_clay_formations_fab.robots._scripts import compose_up_driver

log: logging.Logger = logging.getLogger(__name__)


def fabrication(run_conf: confuse.AttrDict, run_data: dict) -> None:
    """Fabrication runner placing elements according to fab_data and conf."""

    try:
        run_data_path = run_conf.run_data_path
        # this regex strips rotation numbers of file path, i.e test.log.01 --> test.log
        _clean_file_name = re.sub(r"\.\d+", "", run_data_path.name)
        run_data_path = run_data_path.with_name(_clean_file_name)

        dump_worker = DumpThread(run_data_path, run_data)
        dump_worker.start()

        place_future_queue: Queue = Queue(maxsize=2)
        WaitOnCycleTimeThread(place_future_queue).start()

        watch_future_queue: Queue = Queue()
        WaitOnFutureThread(watch_future_queue).start()

        compose_worker = threading.Thread(
            target=compose_up_driver, args=[run_conf.robot_client.controller]
        )
        compose_worker.start()

        # setup fab data
        fab_elements = run_data["fab_data"]

        log.info(f"{len(fab_elements)} fabrication elements.")

        pick_station = run_data["pick_station"]

        # Uses RotatingFileHandler to do a rollover to keep old versions of
        # run_data
        _handler = RotatingFileHandler(run_data_path, maxBytes=1, backupCount=100)
        _handler.doRollover()
        _handler.close()
        # Finally dump run_data again to not confuse user with an empty file
        dump_worker.dump_flag.set()

        _edit_sequence(fab_elements)

        compose_worker.join()

        # Start abb client
        with AbbRcfFabricationClient(run_conf.robot_client, pick_station) as rob_client:
            rob_client.ensure_connection()

            # Confirm start on flexpendant
            rob_client.confirm_start()

            # Set speed, accel, tool, wobj and move to start pos
            rob_client.pre_procedure()

            # Fabrication loop
            for i, elem in enumerate(fab_elements):
                if elem._skip:
                    continue

                # Setup log message and flex pendant message
                log_msg = f"{i}/{len(fab_elements) - 1}, id {elem.id_}."
                log.info(f"Sending {log_msg}")

                pendant_msg = f"{datetime.now().strftime('%H:%M')}: Executing {log_msg}"
                rob_client.send(PrintTextNoErase(pendant_msg))

                # Start clock and send instructions
                rob_client.send(compas_rrc.StartWatch())
                rob_client.pick_element()

                prev_elem: PlaceElement = fab_elements[i - 1]
                if prev_elem.cycle_time:
                    cycle_time_msg = f"Last cycle time was: {prev_elem.cycle_time:0.0f}"
                    log.info(cycle_time_msg)
                    rob_client.send(PrintTextNoErase(cycle_time_msg))

                place_future = rob_client.place_element(elem)

                # set placed to mark progress
                elem.placed = True

                # log time sent
                elem.time_sent = datetime.now().timestamp()

                # Put place future in queue, this will block if queue is full
                place_future_queue.put(place_future)

                elem._cycle_time_future = rob_client.send(compas_rrc.StopWatch())
                watch_future_queue.put(elem)

        # Wait on last element
        while not place_future_queue.empty() and not watch_future_queue.empty():
            time.sleep(2)

        # Send robot to safe end position and close connection
        rob_client.post_procedure()

    except KeyboardInterrupt:
        log.warn("Stopping fabrication loop and writing progress to file.")
        compose_worker.join()
        # go to the finally block on ctrl - c

    else:  # handle finished run
        dump_worker.file_ = run_data_path.with_name(run_data_path.name + ".99done")

    finally:
        # Shutdown dump worker (includes a dump as well)
        dump_worker.shutdown_flag.set()

        dump_worker.join()


def _edit_sequence(run_data: RunData) -> None:
    """Edit placed marker for fabrication elements.

    Parameters
    ----------
    fab_elems
        List of fabrication elements.
    """
    fab_elems = run_data.fab_data

    def _set_skip_before_idx(idx: int) -> None:
        for i, elem in enumerate(fab_elems):
            elem.skip = i < idx

            log.debug(f"Element with index {i} and id {elem.id_} marked {elem.skip}")

    def ignore_placed() -> None:
        for i, elem in enumerate(fab_elems):
            elem.skip = False
            log.debug(f"Element with index {i} and id {elem.id_} marked {elem.skip}")

    def set_start_idx() -> None:
        idx = questionary.text(
            "From which index would you like to start?",
            validate=lambda val: val.isdigit() and 0 <= int(val) < len(fab_elems),
        ).ask()
        _set_skip_before_idx(int(idx))

    def respect_placed() -> None:
        # Take the last element marked as placed
        idx = [i for i, elem in enumerate(fab_elems) if elem.placed]
        _set_skip_before_idx(idx[-1] + 1)

    def selection_ui() -> None:
        selection = questionary.checkbox(
            "Select fabrication elements to place:",
            [
                f"{i:03} (id {elem.id_}), marked placed: {bool(elem.placed)}"
                for i, elem in enumerate(fab_elems)
            ],
        ).ask()
        selection_idx = [int(elem.split()[0]) for elem in selection]

        for i, elem in enumerate(fab_elems):
            elem.skip = i not in selection_idx
            log.debug(f"Element with index {i} and id {elem.id_} marked {elem.skip}")

    func_desc = {
        ignore_placed: "Place all.",
        selection_ui: "Select which elements to place manually",
        respect_placed: "Start after the last element marked as placed.",
        set_start_idx: "Select start index.",
    }

    possible_funcs = [ignore_placed, selection_ui, set_start_idx]

    marked_placed_idx = [i for i in range(len(fab_elems)) if fab_elems[i].placed]

    log.info(f"{len(marked_placed_idx)} elements have been marked as placed.")

    if len(marked_placed_idx) > 0:
        possible_funcs.insert(0, respect_placed)

        last_marked_placed_idx = marked_placed_idx[-1]
        last_marked_placed = fab_elems[last_marked_placed_idx]

        log.info(
            "Last fabrication element marked as placed was "
            + f"{last_marked_placed_idx:03}/{len(fab_elems):03} "
            + f"with id {last_marked_placed.id_}."
        )
    else:
        log.info("No elements have been marked as placed.")

    selected_desc = questionary.select(
        "Please select how to proceed.",
        [func_desc[func] for func in possible_funcs],
    ).ask()

    log.debug(f"{selected_desc} was choosen.")

    desc_func = {v: k for k, v in func_desc.items()}  # inverted dict
    desc_func[selected_desc]()  # type: ignore


class WaitOnFutureThread(threading.Thread):
    def __init__(self, queue, callback=None):
        super().__init__(daemon=True)
        self.queue = queue
        self.callback = callback

    def run(self):
        while True:
            future = self.queue.get()  # blocks until something is put in queue
            self.process_item(future)

            self.queue.task_done()

    def process_item(self, item, *args):
        item.result()  # blocks until robot has given feedback
        if self.callback:
            self.callback()


class WaitOnCycleTimeThread(WaitOnFutureThread):
    def __init__(self, queue):
        super().__init__(queue)

    def process_item(item):
        item.cycle_time = item._cycle_time_future.result()


class DumpThread(threading.Thread):
    def __init__(self, file_, data, encoder=DataEncoder):
        super().__init__()
        self.file_ = file_
        self.data = data
        self.encoder = encoder

        self.dump_flag = threading.Event()
        self.shutdown_flag = threading.Event()

    def run(self):
        while True:
            if self.dump_flag:
                self.dump()
                self.dump_flag.clear()
            elif self.shutdown_flag:
                self.dump()
                break
            else:
                time.sleep(2)

    def dump(self):
        with self.file_.open(mode="w") as fp:
            json.dump(self.data, fp, cls=self.encoder)
        log.debug(f"Wrote run_data to {self.file_}.")
