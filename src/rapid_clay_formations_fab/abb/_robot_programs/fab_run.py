from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import logging
import re
import time

import questionary
from compas.geometry import Transformation
from compas_fab.backends.ros import RosClient
from compas_rrc import PrintText

from rapid_clay_formations_fab.abb import AbbRcfClient
from rapid_clay_formations_fab.abb._robot_programs import compose_up_driver
from rapid_clay_formations_fab.abb._robot_programs import confirm_start
from rapid_clay_formations_fab.fab_data import FabricationElement
from rapid_clay_formations_fab.fab_data import PickStation
from rapid_clay_formations_fab.localization import publish_static_transform
from rapid_clay_formations_fab.utils import CompasObjEncoder

log = logging.getLogger(__name__)


def _edit_fab_data(fab_elems, run_conf):
    """Edit placed marker for fabrication elements.

    Parameters
    ----------
    fab_elems : list of :class:`rapid_clay_formations_fab.fab_data.FabricationElement`
        List of fabrication elements.
    """  # noqa: E501

    def set_placed_list(idx_last_placed):
        for i, elem in enumerate(fab_elems):
            if i <= idx_last_placed:
                elem.placed = True
            else:
                elem.placed = False
            log.debug(
                f"Element with index {i} and id {elem.bullet_id} marked {elem.placed}"
            )

    def selection_ui():
        not_placed_selection = questionary.checkbox(
            "Select fabrication elements to place:",
            [
                f"{i:03} (id {elem.bullet_id}), marked placed: {bool(elem.placed)}"
                for i, elem in enumerate(fab_elems)
            ],
        ).ask()
        mark_not_placed_idx = [int(elem.split()[0]) for elem in not_placed_selection]

        for i, elem in enumerate(fab_elems):
            if i in mark_not_placed_idx:
                elem.placed = False
            else:
                elem.placed = True
            log.debug(
                f"Element with index {i} and id {elem.bullet_id} marked {elem.placed}"
            )

    choice_desc = {
        "ignore_placed": "Place all.",
        "selection_ui": "Select which elements to place manually",
        "respect_placed": "Start after the last element marked as placed.",
        "set_start_idx": "Select start index.",
    }

    possible_choices = ["ignore_placed", "selection_ui", "set_start_idx"]

    marked_placed_idx = [i for i in range(len(fab_elems)) if fab_elems[i].placed]

    log.info("{} elements have been marked as placed.".format(len(marked_placed_idx)))

    if len(marked_placed_idx) == 0 and not run_conf.edit_sequence:
        return

    if len(marked_placed_idx) > 0:
        possible_choices.insert(0, "respect_placed")

        last_marked_placed_idx = marked_placed_idx[-1]
        last_marked_placed = fab_elems[last_marked_placed_idx]

        log.info(
            "Last fabrication element marked as placed was {:03}/{:03} with id {}.".format(  # noqa: E501
                last_marked_placed_idx, len(fab_elems) - 1, last_marked_placed.bullet_id
            )
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


def _publish_tf_static_xform(xform=None):
    """Start a docker service advertising  a TF2 static transformation.

    Parameters
    ----------
    xform : :obj:`list` of :obj:`list` of :obj:`float`, optional
        Transformation matrix. Defaults to a zero-matrix.
    """
    if xform:
        xform = Transformation.from_data(xform)
        log.debug("Loading matrix from run_data.")
    else:
        xform = Transformation()
        log.debug("Publishing zero matrix")

    publish_static_transform(xform, scale_factor=1000)  # mm to m scale factor


def fab_run(run_conf, run_data):
    """Fabrication runner, sets conf, reads json input and runs fabrication process."""
    # Publish TF static transform for transformation by ROS
    if run_conf.publish_tf_xform:
        _publish_tf_static_xform(xform=run_data.get("xform"))

    compose_up_driver(run_conf.robot_client.controller)

    # setup fab data
    fab_elements = [FabricationElement.from_data(data) for data in run_data["fab_data"]]
    log.info("Fabrication data read.")

    log.info(f"{len(fab_elements)} fabrication elements..")

    # Setup pick station
    with run_conf.pick_conf.open(mode="r") as fp:
        pick_station = PickStation.from_data(json.load(fp))
    log.info(f"Pick station setup read from {run_conf.pick_conf}")

    run_data_path = run_conf.run_data_path

    # setup in_progress JSON
    progress_identifier = "-IN_PROGRESS"

    progress_identifier_regex = re.compile(progress_identifier + r"\d{0,2}")

    if progress_identifier in run_data_path.stem:
        progress_file = run_data_path
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
        progress_file = run_data_path.with_name(
            run_data_path.stem + progress_identifier + run_data_path.suffix
        )

    log.info(f"Progress will be saved to {progress_file}.")

    done_file_name = re.sub(progress_identifier_regex, "-DONE", progress_file.name)
    done_file = progress_file.with_name(done_file_name)

    # Fabrication loop
    _edit_fab_data(fab_elements, run_conf)

    # Create Ros Client
    with RosClient(port=9090) as ros:

        # Create AbbRcf client (subclass of AbbClient)
        rob_client = AbbRcfClient(ros, run_conf.robot_client)

        confirm_start()

        rob_client.check_reconnect()

        # Set speed, accel, tool, wobj and move to start pos
        rob_client.pre_procedure()

        # Initialize this before first run, it gets set after placement
        cycle_time_msg = None

        for i, fab_element in enumerate(fab_elements):
            if fab_element.placed:
                continue
            current_elem_desc = (
                f"{i}/{len(fab_elements) - 1}, id {fab_element.bullet_id}."
            )
            log.info(current_elem_desc)

            pendant_msg = ""

            if cycle_time_msg:
                pendant_msg += cycle_time_msg + " "
            pendant_msg += current_elem_desc

            # TP write limited to 40 char / line
            rob_client.send(PrintText(pendant_msg[:40]))

            pick_element = pick_station.get_next_pick_elem(fab_element)

            # Send instructions and store feedback obj
            pick_future = rob_client.pick_element(pick_element)
            place_future = rob_client.place_element(fab_element)

            # set placed to temporary value to mark it as "placed"
            fab_element.placed = True

            # Write progress to json while waiting for robot
            run_data["fab_data"] = fab_elements
            with progress_file.open(mode="w") as fp:
                json.dump(run_data, fp, cls=CompasObjEncoder)
            log.debug(f"Wrote fabrication data to {progress_file.name}")

            # This blocks until cycle is finished
            cycle_time = pick_future.result() + place_future.result()

            fab_element.cycle_time = cycle_time
            # format float to int to save characters on teach pendant
            cycle_time_msg = f"Last cycle time: {fab_element.cycle_time:0.0f}"
            log.info(cycle_time_msg)

            fab_element.time_placed = time.time()
            log.debug(f"Time placed was {fab_element.time_placed}")

        # Write progress of last run of loop
        run_data["fab_data"] = fab_elements
        with done_file.open(mode="w") as fp:
            json.dump(run_data, fp, cls=CompasObjEncoder)
        log.info("Wrote final run_data to {}".format(done_file.name))

        rob_client.post_procedure()
