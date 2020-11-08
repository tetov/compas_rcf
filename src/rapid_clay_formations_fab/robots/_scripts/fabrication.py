"""Fabrication runner placing elements according to fab_data and conf."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Sequence
from typing import Tuple

import confuse
import questionary

import rapid_clay_formations_fab.robots as rcf_robots
from rapid_clay_formations_fab.fab_data import PlaceElement
from rapid_clay_formations_fab.robots import AbbRcfFabricationClient
from rapid_clay_formations_fab.robots._scripts import compose_up_driver
from rapid_clay_formations_fab.utils import CompasObjEncoder

log: logging.Logger = logging.getLogger(__name__)


def fabrication(run_conf: confuse.AttrDict, run_data: dict) -> None:
    """Fabrication runner placing elements according to fab_data and conf."""

    compose_up_driver(run_conf.robot_client.controller)

    # setup fab data
    fab_elements = [PlaceElement.from_data(data) for data in run_data["fab_data"]]
    log.info("Fabrication data read.")

    log.info(f"{len(fab_elements)} fabrication elements.")

    pick_station = rcf_robots.PickStation.from_data(run_data["pick_station"])

    progress_file, done_file = _setup_file_paths(run_conf.run_data_path)

    _edit_fab_data(fab_elements, run_conf)

    # Start abb client
    with AbbRcfFabricationClient(run_conf.robot_client, pick_station) as rob_client:
        rob_client.check_reconnect()

        # Confirm start on flexpendant
        rob_client.confirm_start()

        # Set speed, accel, tool, wobj and move to start pos
        rob_client.pre_procedure()

        # Initialize this before first run, it gets set after placement
        cycle_time_msg = None

        # Fabrication loop
        for i, elem in enumerate(fab_elements):
            if elem.placed:  # Don't place elements that are marked as placed
                continue

            # Setup log message and flex pendant message
            current_elem_desc = f"{i}/{len(fab_elements) - 1}, id {elem.id_}."
            log.info(current_elem_desc)

            # Having this as an f-string should mean that the timestamp will
            # be set when the PrintText command is sent
            pendant_msg = f"{datetime.now().strftime('%H:%M')} "
            if cycle_time_msg:
                pendant_msg += cycle_time_msg
            pendant_msg += current_elem_desc

            # TP write limited to 40 char / line
            rob_client.send(rcf_robots.PrintTextNoErase(pendant_msg[:40]))

            # Send instructions and store feedback obj
            pick_future = rob_client.pick_element()
            place_future = rob_client.place_element(elem)

            # set placed to true right after pick elem
            elem.placed = True

            # Write progress to json while waiting for robot
            run_data["fab_data"] = fab_elements
            with progress_file.open(mode="w") as fp:
                json.dump(run_data, fp, cls=CompasObjEncoder)
            log.debug(f"Wrote fabrication data to {progress_file.name}")

            # This blocks until cycle is finished
            elem.cycle_time = pick_future.result() + place_future.result()

            # format float to int to save characters on teach pendant
            cycle_time_msg = f"LC {elem.cycle_time:0.0f}, "
            log.info(f"Last cycle time was: {elem.cycle_time:0.0f}")

            elem.time_placed = datetime.now().timestamp()
            log.debug(f"Time placed was {elem.time_placed}")

        # Write progress of last run of loop
        run_data["fab_data"] = fab_elements
        with done_file.open(mode="w") as fp:
            json.dump(run_data, fp, cls=CompasObjEncoder)
        log.info(f"Wrote final run_data to {done_file}")

        # Send robot to safe end position and close connection
        rob_client.post_procedure()


def _edit_fab_data(
    fab_elems: Sequence[PlaceElement], run_conf: confuse.AttrDict
) -> None:
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

    if len(marked_placed_idx) == 0 and not run_conf.edit_sequence:
        return

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
