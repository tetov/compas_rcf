from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import logging
import re
import time
from operator import attrgetter

import questionary
from compas.geometry import Transformation
from compas_fab.backends.ros import RosClient
from compas_rrc import PrintText

from compas_rcf.abb import AbbRcfClient
from compas_rcf.abb._robot_programs import compose_up_driver
from compas_rcf.abb._robot_programs import confirm_start
from compas_rcf.fab_data import ClayBullet
from compas_rcf.fab_data import PickStation
from compas_rcf.localization import publish_static_transform
from compas_rcf.utils import CompasObjEncoder

log = logging.getLogger(__name__)


def _check_fab_data(clay_bullets):
    """Check for placed bullets in JSON.

    Parameters
    ----------
    clay_bullets : list of :class:`compas_rcf.fabrication.clay_objs.ClayBullet`
        Original list of ClayBullets.

    Returns
    -------
    list of :class:`compas_rcf.fabrication.clay_objs.ClayBullet`
        Curated list of ClayBullets
    """
    maybe_placed = [bullet for bullet in clay_bullets if bullet.placed is not None]

    if len(maybe_placed) < 1:
        return clay_bullets

    last_placed = max(maybe_placed, key=attrgetter("bullet_id"))
    last_placed_index = clay_bullets.index(last_placed)

    log.info(
        "Last bullet placed was {:03}/{:03} with id {}.".format(
            last_placed_index, len(clay_bullets), last_placed.bullet_id
        )
    )

    skip_options = questionary.select(
        "Some or all bullet seems to have been placed already.",
        [
            "Skip all bullet marked as placed in JSON file.",
            "Place all anyways.",
            questionary.Separator(),
            "Place some of the bullets.",
        ],
    ).ask()

    if skip_options == "Skip all bullet marked as placed in JSON file.":
        to_place = [bullet for bullet in clay_bullets if bullet not in maybe_placed]
    if skip_options == "Place all anyways.":
        to_place = clay_bullets[:]
    if skip_options == "Place some of the bullets.":
        skip_method = questionary.select(
            "Select method:",
            ["Place last N bullets again.", "Pick bullets to place again."],
        ).ask()
        if skip_method == "Place last N bullets again.":
            n_place_again = questionary.text(
                "Number of bullets from last to place again?",
                "1",
                lambda val: val.isdigit() and -1 < int(val) < last_placed_index,
            ).ask()
            to_place = clay_bullets[last_placed_index - int(n_place_again) + 1 :]
            log.info(
                "Placing last {} bullets again. First bullet will be id {}.".format(
                    n_place_again, to_place[0].bullet_id,
                )
            )
        else:
            to_place_selection = questionary.checkbox(
                "Select bullets:",
                [
                    "{:03} (id {}), marked placed: {}".format(
                        i, bullet.bullet_id, bullet.placed is not None
                    )
                    for i, bullet in enumerate(clay_bullets)
                ],
            ).ask()
            indices = [int(bullet.split()[0]) for bullet in to_place_selection]
            to_place = [clay_bullets[i] for i in indices]

    return to_place


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
    clay_cylinders = [ClayBullet.from_data(data) for data in run_data["fab_data"]]
    log.info("Fabrication data read.")

    log.info(f"{len(clay_cylinders)} items in clay_cylinders.")

    # setup pick station
    # TODO: Integrate into AbbRcfClient?
    with run_conf.pick_conf.open(mode="r") as fp:
        pick_station = PickStation.from_data(json.load(fp))

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

    done_file_name = re.sub(progress_identifier_regex, "-DONE", progress_file.name)
    done_file = progress_file.with_name(done_file_name)

    # Create Ros Client                                                        #
    with RosClient() as ros:

        # Create AbbRcf client (subclass of AbbClient)
        rob_client = AbbRcfClient(ros, run_conf.robot_client)

        rob_client.check_reconnect()

        # Fabrication loop
        to_place = _check_fab_data(clay_cylinders)

        confirm_start()

        # Set speed, accel, tool, wobj and move to start pos
        rob_client.pre_procedure()

        for bullet in to_place:
            bullet.placed = None
            bullet.cycle_time = None

        for i, bullet in enumerate(to_place):
            current_bullet_desc = "Bullet {:03}/{:03} with id {}.".format(
                i, len(to_place) - 1, bullet.bullet_id
            )

            rob_client.send(PrintText(current_bullet_desc))
            log.info(current_bullet_desc)

            pick_frame = pick_station.get_next_frame(bullet)

            # Pick bullet
            pick_future = rob_client.pick_bullet(pick_frame)

            # Place bullet
            place_future = rob_client.place_bullet(bullet)

            bullet.placed = 1  # set placed to temporary value to mark it as "placed"

            # Write progress to json while waiting for robot
            run_data["fab_data"] = [cylinder.to_data() for cylinder in clay_cylinders]
            with progress_file.open(mode="w") as fp:
                json.dump(run_data, fp, cls=CompasObjEncoder)
            log.debug("Wrote clay_bullets to {}".format(progress_file.name))

            # This blocks until cycle is finished
            cycle_time = pick_future.result() + place_future.result()

            bullet.cycle_time = cycle_time
            log.debug("Cycle time was {}".format(bullet.cycle_time))
            bullet.placed = time.time()
            log.debug("Time placed was {}".format(bullet.placed))

        # Write progress of last run of loop
        run_data["fab_data"] = [cylinder.to_data() for cylinder in clay_cylinders]
        with progress_file.open(mode="w") as fp:
            json.dump(run_data, fp, cls=CompasObjEncoder)
        log.debug("Wrote run_data to {}".format(progress_file.name))

        if len([bullet for bullet in clay_cylinders if bullet.placed is None]) == 0:
            progress_file.rename(done_file)
            log.debug(f"Progressfile renamed to {done_file}.")

        rob_client.post_procedure()
