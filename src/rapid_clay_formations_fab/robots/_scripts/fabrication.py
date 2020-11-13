"""Fabrication runner placing elements according to fab_data and conf."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import logging
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple
import sys

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

    compose_up_driver(run_conf.robot_client.controller)

    # setup fab data
    fab_elements = run_data["fab_data"]

    log.info(f"{len(fab_elements)} fabrication elements.")

    pick_station = run_data["pick_station"]

    progress_file, done_file = _setup_file_paths(run_conf.run_data_path)

    _edit_fab_data(fab_elements)

    prev_elem: Optional[PlaceElement] = None

    # Start abb client
    with AbbRcfFabricationClient(run_conf.robot_client, pick_station) as rob_client:
        rob_client.ensure_connection()

        # Confirm start on flexpendant
        rob_client.confirm_start()

        # Set speed, accel, tool, wobj and move to start pos
        rob_client.pre_procedure()

        i = 0
        # Fabrication loop
        for i, elem in enumerate(fab_elements):
            if elem.placed:  # Don't place elements that are marked as placed
                continue

            # Setup log message and flex pendant message
            log_msg = f"{i}/{len(fab_elements) - 1}, id {elem.id_}."
            log.info(log_msg)

            # Having this as an f-string should mean that the timestamp will
            # be set when the PrintText command is sent
            pendant_msg = f"{datetime.now().strftime('%H:%M')}: {log_msg}"

            rob_client.send(PrintTextNoErase(pendant_msg))

            # Start clock and send instructions
            rob_client.send(compas_rrc.StartWatch())
            rob_client.pick_element()

            # Save cycle time from last run
            # The main reason though is to stop the fabrication loop until
            # confirmation that last loop finished. It is done between pick
            # instructions and place instructions to (hopefully) make sure the
            # robot always has instructions to execute

            if prev_elem and prev_elem.cycle_time_future:  # Is there a clock to check?
                prev_elem.cycle_time = _wait_and_return_future(
                    prev_elem.cycle_time_future
                )

                # TODO: Move sysexit to _wait_and_return_future here?
                if not prev_elem.cycle_time:  # If KeyboardInterrupt was raised
                    log.info("Exiting script, breaking loop and saving run_data.")
                    _write_run_data(progress_file, run_data, fab_elements)
                    sys.exit(0)

                cycle_time_msg = f"Last cycle time was: {prev_elem.cycle_time:0.0f}"
                log.info(cycle_time_msg)
                rob_client.send(PrintTextNoErase(cycle_time_msg))

                prev_elem.time_placed = datetime.now().timestamp()
                log.debug(f"Time prev elem was placed: {elem.time_placed}")

            rob_client.place_element(elem)
            rob_client.send(compas_rrc.StopWatch())

            elem.cycle_time_future = rob_client.send(compas_rrc.ReadWatch())

            # set placed to mark progress
            elem.placed = True

            # Write progress to json while waiting for robot
            _write_run_data(progress_file, run_data, fab_elements)

            prev_elem = elem

        # Wait on last element
        if prev_elem and prev_elem.cycle_time_future:
            prev_elem.cycle_time = _wait_and_return_future(prev_elem.cycle_time_future)

        # Write progress of last run of loop
        # First figure out if the file should be labeled done though.
        _placed_is_true = filter(lambda x: x.placed, fab_elements)
        if len(list(_placed_is_true)) == len(fab_elements):
            _file = done_file
        else:
            _file = progress_file

        _write_run_data(_file, run_data, fab_elements)

        # Send robot to safe end position and close connection
        rob_client.post_procedure()


def _wait_and_return_future(future: compas_rrc.FutureResult) -> Any:
    try:
        while future.done is False:
            time.sleep(3)
    except KeyboardInterrupt:
        return

    return future.result()


def _write_run_data(
    file_: Path, run_data: dict, fab_elements: List[PlaceElement]
) -> None:
    run_data["fab_data"] = fab_elements
    with file_.open(mode="w") as fp:
        json.dump(run_data, fp, cls=DataEncoder)
    log.info(f"Wrote run_data to {file_}.")


def _edit_fab_data(fab_elems: List[PlaceElement]) -> None:
    """Edit placed marker for fabrication elements.

    Parameters
    ----------
    fab_elems : list of :class:`rapid_clay_formations_fab.fabrication.clay_objs.ClayBullet`
        List of fabrication elements.
    """  # noqa: E501

    def set_placed_list(idx_last_placed: int) -> None:
        for i, elem in enumerate(fab_elems):
            if i <= idx_last_placed:
                elem.placed = True
            else:
                elem.placed = False
            log.debug(f"Element with index {i} and id {elem.id_} marked {elem.placed}")

    def selection_ui() -> None:
        not_placed_selection = questionary.checkbox(
            "Select fabrication elements to place:",
            [
                f"{i:03} (id {elem.id_}), marked placed: {bool(elem.placed)}"
                for i, elem in enumerate(fab_elems)
            ],
        ).ask()
        mark_not_placed_idx = [int(elem.split()[0]) for elem in not_placed_selection]

        for i, elem in enumerate(fab_elems):
            if i in mark_not_placed_idx:
                elem.placed = False
            else:
                elem.placed = True
            log.debug(f"Element with index {i} and id {elem.id_} marked {elem.placed}")

    choice_desc = {
        "ignore_placed": "Place all.",
        "selection_ui": "Select which elements to place manually",
        "respect_placed": "Start after the last element marked as placed.",
        "set_start_idx": "Select start index.",
    }

    possible_choices = ["ignore_placed", "selection_ui", "set_start_idx"]

    marked_placed_idx = [i for i in range(len(fab_elems)) if fab_elems[i].placed]

    log.info(f"{len(marked_placed_idx)} elements have been marked as placed.")

    if len(marked_placed_idx) > 0:
        possible_choices.insert(0, "respect_placed")

        last_marked_placed_idx = marked_placed_idx[-1]
        last_marked_placed = fab_elems[last_marked_placed_idx]

        log.info(
            "Last fabrication element marked as placed was "
            + f"{last_marked_placed_idx:03}/{len(fab_elems):03} "
            + f"with id {last_marked_placed.id_}."
        )

    selected_desc = questionary.select(
        "Please select how to proceed.",
        [choice_desc[choice] for choice in possible_choices],
    ).ask()

    log.debug(f"{selected_desc} was choosen.")

    if selected_desc == choice_desc["ignore_placed"]:
        set_placed_list(-1)
    elif selected_desc == choice_desc["respect_placed"]:
        set_placed_list(last_marked_placed_idx)
    elif selected_desc == choice_desc["set_start_idx"]:
        idx = questionary.text(
            "From which index would you like to start?",
            validate=lambda val: val.isdigit() and 0 <= int(val) < len(fab_elems),
        ).ask()
        set_placed_list(int(idx) - 1)
    else:
        selection_ui()


def _setup_file_paths(input_file_path: Path) -> Tuple[Path, Path]:
    # setup in_progress JSON
    progress_identifier = "-IN_PROGRESS"

    progress_identifier_regex = re.compile(progress_identifier + r"\d{0,2}")

    if progress_identifier in input_file_path.stem:
        progress_file = input_file_path
        i = 1
        # Add number and increment it if needed.
        while progress_file.exists():
            # strip suffix
            stem = progress_file.stem

            # Match IN_PROGRESS with or without digits after and add/replace digits
            new_name = re.sub(
                progress_identifier_regex, progress_identifier + f"{i:02}", stem
            )

            new_name += progress_file.suffix

            progress_file = progress_file.with_name(new_name)

            i += 1
    else:
        progress_file = input_file_path.with_name(
            input_file_path.stem + progress_identifier + input_file_path.suffix
        )

    log.info(f"Progress will be saved to {progress_file}.")

    done_file_name = re.sub(progress_identifier_regex, "-DONE", progress_file.name)
    done_file = progress_file.with_name(done_file_name)

    log.info(f"When run is finished data will be saved to {done_file}.")

    return progress_file, done_file
