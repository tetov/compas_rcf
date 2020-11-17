"""Fabrication runner placing elements according to fab_data and conf."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from typing import Optional
from typing import Tuple

import compas_rrc
import confuse

from rapid_clay_formations_fab.fab_data import PlaceElement
from rapid_clay_formations_fab.robots import AbbRcfFabricationClient
from rapid_clay_formations_fab.robots import PrintTextNoErase
from rapid_clay_formations_fab.robots._scripts import compose_up_driver

log: logging.Logger = logging.getLogger(__name__)


def test_fabrication(run_conf: confuse.AttrDict, run_data: dict) -> None:
    """Fabrication runner placing elements according to fab_data and conf."""

    compose_up_driver(run_conf.robot_client.controller)

    # setup fab data
    fab_elements = run_data["fab_data"]

    log.info(f"{len(fab_elements)} fabrication elements.")

    pick_station = run_data["pick_station"]

    progress_file, done_file = _setup_file_paths(run_conf.run_data_path)

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
        while True:
            place_idx = i % len(fab_elements)
            elem = fab_elements[place_idx]

            pick_msg = f"Picking from position {i}"
            log.info(pick_msg)
            rob_client.send(PrintTextNoErase(pick_msg))

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
                    sys.exit(0)

                cycle_time_msg = f"Last cycle time was: {prev_elem.cycle_time:0.0f}"
                log.info(cycle_time_msg)
                rob_client.send(PrintTextNoErase(cycle_time_msg))

                prev_elem.time_placed = datetime.now().timestamp()
                log.debug(f"Time prev elem was placed: {elem.time_placed}")

            rob_client.place_element(elem)

            place_msg = f"Placing element {place_idx + 1}/{len(fab_elements)}"
            log.info(place_msg)
            rob_client.send(PrintTextNoErase(place_msg))
            rob_client.send(compas_rrc.StopWatch())

            elem.cycle_time_future = rob_client.send(compas_rrc.ReadWatch())

            # set placed to mark progress
            elem.placed = True

            prev_elem = elem

            i += 1

        # Send robot to safe end position and close connection
        rob_client.post_procedure()


def _wait_and_return_future(future: compas_rrc.FutureResult) -> Any:
    try:
        while future.done is False:
            time.sleep(3)
    except KeyboardInterrupt:
        return

    return future.result()


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
