"""Fabrication runner for Rapid Clay Fabrication project for fullscale structure.

Run from command line using :code:`python -m compas_rcf.abb.run`
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import logging as log
import sys
import time
from datetime import datetime
from operator import attrgetter

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector
from compas_fab.backends.ros import RosClient
from compas_rrc import AbbClient
from compas_rrc import PrintText

from compas_rcf import __version__
from compas_rcf.abb import DOCKER_COMPOSE_PATHS
from compas_rcf.abb import ROBOT_IPS
from compas_rcf.abb import check_reconnect
from compas_rcf.abb import pick_bullet
from compas_rcf.abb import place_bullet
from compas_rcf.abb import post_procedure
from compas_rcf.abb import pre_procedure
from compas_rcf.docker import compose_up
from compas_rcf.fab_data import ClayBulletEncoder
from compas_rcf.fab_data import fab_conf
from compas_rcf.fab_data import interactive_conf_setup
from compas_rcf.fab_data import load_bullets
from compas_rcf.fab_data.conf import Path
from compas_rcf.utils import open_file_dialog

if sys.version_info[0] < 2:
    raise Exception("This module requires Python 3")
else:
    import questionary


def pick_frame_from_grid(index, bullet_height):
    """Get next picking frame.

    Parameters
    ----------
    index : int
        Counter to iterate through picking positions.
    bullet_height : float
        Height of bullet to pick up.

    Returns
    -------
    list of `class`:compas.geometry.Frame
    """
    # If index is larger than amount on picking plate, start from zero again
    index = index % (fab_conf["pick"]["xnum"].get() * fab_conf["pick"]["ynum"].get())

    xpos = index % fab_conf["pick"]["xnum"].get()
    ypos = index // fab_conf["pick"]["xnum"].get()

    x = (
        fab_conf["pick"]["origin_grid"]["x"].get()
        + xpos * fab_conf["pick"]["grid_spacing"].get()
    )
    y = (
        fab_conf["pick"]["origin_grid"]["y"].get()
        + ypos * fab_conf["pick"]["grid_spacing"].get()
    )
    z = bullet_height * fab_conf["pick"]["compression_height_factor"].get()

    frame = Frame(
        Point(x, y, z),
        Vector(*fab_conf["pick"]["xaxis"].get()),
        Vector(*fab_conf["pick"]["yaxis"].get()),
    )
    log.debug("Picking frame {:03d}: {}".format(index, frame))
    return frame


def logging_setup():
    """Configure logging for module and imported modules."""
    timestamp_file = datetime.now().strftime("%Y%m%d-%H.%M_rcf_abb.log")
    log_file = fab_conf["paths"]["log_dir"].get(Path()) / timestamp_file

    handlers = []

    if not fab_conf["skip_logfile"].get():
        handlers.append(log.FileHandler(log_file, mode="a"))
    if fab_conf["quiet"].get() is not True:
        handlers.append(log.StreamHandler(sys.stdout))

    log.basicConfig(
        level=log.DEBUG if fab_conf["debug"].get() else log.INFO,
        format="%(asctime)s:%(levelname)s:%(funcName)s:%(message)s",
        handlers=handlers,
    )


def setup_fab_data(clay_bullets):
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


################################################################################
# Script runner                                                                #
################################################################################
def main():
    """Fabrication runner, sets conf, reads json input and runs fabrication process."""
    # CONF setup
    interactive_conf_setup()

    ############################################################################
    # Docker setup                                                            #
    ############################################################################
    compose_up(DOCKER_COMPOSE_PATHS["base"], check_output=True, remove_orphans=False)
    log.debug("Compose up master and bridge")
    ip = {"ROBOT_IP": ROBOT_IPS[fab_conf["target"].as_str()]}
    compose_up(DOCKER_COMPOSE_PATHS["driver"], check_output=True, env_vars=ip)
    log.debug("Compose up abb_driver")

    ############################################################################
    # Load fabrication data                                                    #
    ############################################################################
    json_path = open_file_dialog(
        title="Specify fabrication file",
        initial_dir=fab_conf["paths"]["json_dir"].get(),
        file_type=("JSON files", "*.json"),
        return_pathobj=True,
    )
    clay_bullets = load_bullets(json_path)
    log.info("Fabrication data read from: {}".format(json_path))
    log.info("{} items in clay_bullets.".format(len(clay_bullets)))

    ############################################################################
    # Create Ros Client                                                        #
    ############################################################################
    ros = RosClient()

    ############################################################################
    # Create ABB Client                                                        #
    ############################################################################
    abb = AbbClient(ros)
    abb.run()
    log.debug("Connected to ROS")

    check_reconnect(
        abb,
        target=fab_conf["target"].get(),
        timeout_ping=fab_conf["docker"]["timeout_ping"].get(),
        wait_after_up=fab_conf["docker"]["sleep_after_up"].get(),
    )

    ############################################################################
    # setup in_progress JSON                                                   #
    ############################################################################
    if not fab_conf["skip_progress_file"]:
        json_progress_identifier = "IN_PROGRESS-"

        if json_path.name.startswith(json_progress_identifier):
            in_progress_json = json_path
        else:
            in_progress_json = json_path.with_name(
                json_progress_identifier + json_path.name
            )

    ############################################################################
    # Fabrication loop                                                         #
    ############################################################################

    to_place = setup_fab_data(clay_bullets)

    if not questionary.confirm("Ready to start program?").ask():
        log.critical("Program exited because user didn't confirm start.")
        print("Exiting.")
        sys.exit()

    # Set speed, accel, tool, wobj and move to start pos
    pre_procedure(abb)

    for bullet in to_place:
        bullet.placed = None
        bullet.cycle_time = None

    for i, bullet in enumerate(to_place):
        current_bullet_desc = "Bullet {:03}/{:03} with id {}.".format(
            i, len(to_place) - 1, bullet.bullet_id
        )

        abb.send(PrintText(current_bullet_desc))
        log.info(current_bullet_desc)

        pick_frame = pick_frame_from_grid(i, bullet.height)

        # Pick bullet
        pick_future = pick_bullet(abb, pick_frame)

        # Place bullet
        place_future = place_bullet(abb, bullet)

        bullet.placed = 1  # set placed to temporary value to mark it as "placed"

        # Write progress to json while waiting for robot
        if not fab_conf["skip_progress_file"].get():
            with in_progress_json.open(mode="w") as fp:
                json.dump(clay_bullets, fp, cls=ClayBulletEncoder)
            log.debug("Wrote clay_bullets to {}".format(in_progress_json.name))

        # This blocks until cycle is finished
        cycle_time = pick_future.result() + place_future.result()

        bullet.cycle_time = cycle_time
        log.debug("Cycle time was {}".format(bullet.cycle_time))
        bullet.placed = time.time()
        log.debug("Time placed was {}".format(bullet.placed))

    ############################################################################
    # Shutdown procedure                                                       #
    ############################################################################

    # Write progress of last run of loop
    if not fab_conf["skip_progress_file"].get():
        with in_progress_json.open(mode="w") as fp:
            json.dump(clay_bullets, fp, cls=ClayBulletEncoder)
        log.debug("Wrote clay_bullets to {}".format(in_progress_json.name))

    if (
        len([bullet for bullet in clay_bullets if bullet.placed is None]) == 0
        and not fab_conf["skip_progress_file"].get()
    ):
        done_file_name = json_path.name.replace(json_progress_identifier, "")
        done_json = (
            fab_conf["paths"]["json_dir"].get(Path()) / "00_done" / done_file_name
        )

        in_progress_json.rename(done_json)

        with done_json.open(mode="w") as fp:
            json.dump(clay_bullets, fp, cls=ClayBulletEncoder)

        log.debug("Saved placed bullets to 00_Done.")
    elif not fab_conf["skip_progress_file"].get():
        log.debug(
            "Bullets without placed timestamp still present, keeping {}".format(
                in_progress_json.name
            )
        )

    log.info("Finished program with {} bullets.".format(len(to_place)))

    post_procedure(abb)


if __name__ == "__main__":
    """Entry point, logging setup and argument handling."""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--target",
        choices=["real", "virtual"],
        help="Set fabrication runner target.",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Don't print logging messages to console.",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Log DEBUG level messages."
    )
    parser.add_argument(
        "--skip-logfile", action="store_true", help="Don't send log messages to file.",
    )
    parser.add_argument(
        "--skip-progress-file",
        action="store_true",
        help="Skip writing progress to json during run.",
    )

    args = parser.parse_args()

    fab_conf.set_args(args)

    logging_setup()

    log.info("compas_rcf version: {}".format(__version__))
    log.debug("argparse input: {}".format(args))
    log.debug("config after set_args: {}".format(fab_conf))

    main()
