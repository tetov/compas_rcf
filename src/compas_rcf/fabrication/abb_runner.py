"""Fabrication runner for Rapid Clay Fabrication project for fullscale structure.

Run from command line using :code:`python -m compas_rcf.fabrication.abb_rcf_runner`
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import logging
import sys
import time
from datetime import datetime
from operator import attrgetter
from pathlib import Path

from compas.geometry import Frame
from compas.geometry import Point
from compas.geometry import Vector
from compas_fab.backends.ros import RosClient
from compas_rrc import AbbClient
from compas_rrc import CustomInstruction
from compas_rrc import MoveToFrame
from compas_rrc import MoveToJoints
from compas_rrc import PrintText
from compas_rrc import ReadWatch
from compas_rrc import SetAcceleration
from compas_rrc import SetDigital
from compas_rrc import SetMaxSpeed
from compas_rrc import SetTool
from compas_rrc import SetWorkObject
from compas_rrc import StartWatch
from compas_rrc import StopWatch
from compas_rrc import WaitTime

from compas_rcf import __version__
from compas_rcf.abb.helpers import docker_compose_paths
from compas_rcf.abb.helpers import ping
from compas_rcf.abb.helpers import robot_ips
from compas_rcf.fabrication.clay_obj import ClayBulletEncoder
from compas_rcf.fabrication.conf import abb_rcf_conf_template
from compas_rcf.fabrication.conf import fabrication_conf
from compas_rcf.utils import ui
from compas_rcf.utils.docker import compose_up
from compas_rcf.utils.json_ import load_bullets
from compas_rcf.utils.util_funcs import get_offset_frame

if sys.version_info[0] < 2:
    raise Exception("This module requires Python 3")
else:
    import questionary

################################################################################
# Globals                                                                      #
################################################################################

ROBOT_CONTROL_FOLDER_DRIVE = Path(
    "G:\\Shared drives\\2020_MAS\\T2_P1\\02_Groups\\Phase2\\rcf_fabrication\\02_robot_control"  # noqa E501
)
DEFAULT_CONF_DIR = ROBOT_CONTROL_FOLDER_DRIVE / "05_fabrication_confs"
DEFAULT_JSON_DIR = ROBOT_CONTROL_FOLDER_DRIVE / "04_fabrication_data_jsons"
DEFAULT_LOG_DIR = ROBOT_CONTROL_FOLDER_DRIVE / "06_fabrication_logs"

# Define external axis, will not be used but required in move cmds
EXTERNAL_AXIS_DUMMY: list = []

################################################################################
# Programs                                                                     #
################################################################################


def initial_setup(client):
    """Pre fabrication setup, speed, acceleration, tool, work object and initial pose.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    """
    send_grip_release(client, CONF.tool.release_state)

    client.send(SetTool(CONF.tool.tool_name))
    logging.debug("Tool {} set.".format(CONF.tool.tool_name))
    client.send(SetWorkObject(CONF.wobjs.placing_wobj_name))
    logging.debug("Work object {} set.".format(CONF.wobjs.placing_wobj_name))

    # Set Acceleration
    client.send(SetAcceleration(CONF.speed_values.accel, CONF.speed_values.accel_ramp))
    logging.debug("Acceleration values set.")

    # Set Max Speed
    client.send(
        SetMaxSpeed(CONF.speed_values.speed_override, CONF.speed_values.speed_max_tcp)
    )
    logging.debug("Speed set.")

    # Initial configuration
    client.send(
        MoveToJoints(
            CONF.safe_joint_positions.start,
            EXTERNAL_AXIS_DUMMY,
            CONF.movement.speed_travel,
            CONF.movement.zone_travel,
        )
    )
    logging.debug("Sent move to safe joint position")


def shutdown_procedure(client):
    """Post fabrication procedure, end pose and closing and termination of client.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    """
    send_grip_release(client, CONF.tool.release_state)

    client.send(
        MoveToJoints(
            CONF.safe_joint_positions.end,
            EXTERNAL_AXIS_DUMMY,
            CONF.movement.speed_travel,
            CONF.movement.zone_travel,
        )
    )

    client.send_and_wait(PrintText("Finished"))

    # Close client
    client.close()
    client.terminate()


def send_picking(client, picking_frame):
    """Send movement and IO instructions to pick up a clay bullet.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    picking_frame : compas.geometry.Frame
        Target frame to pick up bullet
    """
    if CONF.target == "virtual":
        # Custom instruction create a clay bullet in RobotStudio
        # TODO: Create bullet at picking point
        client.send(CustomInstruction("r_A057_RS_Create_Bullet"))

    # change work object before picking
    client.send(SetWorkObject(CONF.wobjs.picking_wobj_name))

    # pick bullet
    offset_picking = get_offset_frame(picking_frame, CONF.movement.offset_distance)

    # start watch
    client.send(StartWatch())

    client.send(
        MoveToFrame(
            offset_picking, CONF.movement.speed_travel, CONF.movement.zone_travel
        )
    )

    client.send(
        MoveToFrame(
            picking_frame, CONF.movement.speed_travel, CONF.movement.zone_travel
        )
    )

    send_grip_release(client, CONF.tool.grip_state)

    client.send(
        MoveToFrame(
            offset_picking, CONF.movement.speed_picking, CONF.movement.zone_pick
        )
    )

    client.send(StopWatch())
    return client.send(ReadWatch())


def send_placing(client, bullet):
    """Send movement and IO instructions to place a clay bullet.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    picking_frame : compas.geometry.Frame
        Target frame to pick up bullet
    """
    logging.debug("Location frame: {}".format(bullet.location))

    # change work object before placing
    client.send(SetWorkObject(CONF.wobjs.placing_wobj_name))

    # add offset placing plane to pre and post frames

    top_bullet_frame = get_offset_frame(bullet.location, bullet.height)
    offset_placement = get_offset_frame(top_bullet_frame, CONF.movement.offset_distance)

    # start watch
    client.send(StartWatch())

    # Safe pos then vertical offset
    for frame in bullet.trajectory_to:
        client.send(
            MoveToFrame(frame, CONF.movement.speed_travel, CONF.movement.zone_travel)
        )

    client.send(
        MoveToFrame(
            offset_placement, CONF.movement.speed_travel, CONF.movement.zone_travel
        )
    )
    client.send(
        MoveToFrame(
            top_bullet_frame, CONF.movement.speed_placing, CONF.movement.zone_place
        )
    )

    send_grip_release(client, CONF.tool.release_state)

    client.send(
        MoveToFrame(
            bullet.placement_frame,
            CONF.movement.speed_placing,
            CONF.movement.zone_place,
        )
    )

    client.send(
        MoveToFrame(
            offset_placement, CONF.movement.speed_travel, CONF.movement.zone_travel
        )
    )

    # offset placement frame then safety frame
    for frame in bullet.trajectory_from:
        client.send(
            MoveToFrame(frame, CONF.movement.speed_travel, CONF.movement.zone_travel)
        )

    client.send(StopWatch())
    return client.send(ReadWatch())


def send_grip_release(client, do_state):
    """Grip or release using RCF tool, either in simulation or on real robot.

    If script target is real robot this will set the digital output on the robot,
    and if the target is virtual robot it will use RobotStudio code to visualize
    clay bullet gripping and releasing

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
    do_state : int (0 or 1)
        Value to set DO to
    """
    if CONF.target == "real":
        client.send(WaitTime(CONF.tool.wait_before_io))
        client.send(SetDigital(CONF.tool.io_needles_pin, do_state))
        client.send(WaitTime(CONF.tool.wait_after_io))
    else:
        # Custom instruction can grip a bullet in RobotStudio
        # note the tool tip must touch the bullet
        if do_state == CONF.tool.grip_state:
            client.send(CustomInstruction("r_A057_RS_ToolGrip"))
        else:
            client.send(CustomInstruction("r_A057_RS_ToolRelease"))

    logging.debug(
        "Signal sent to {}".format(
            "grip" if do_state == CONF.tool.grip_state else "release"
        )
    )


################################################################################
# Non programs
################################################################################


def get_settings():
    """Print and prompts user for changes to default configuration.

    Parameters
    ----------
    target_select : str ('real' or 'virtual')
        Target for script, either virtual robot controller or real. From argparse.
    """
    load_or_default = questionary.select(
        "Load config or use default?", choices=["Default", "Load"], default="Default"
    ).ask()

    if load_or_default == "Load":
        conf_file = ui.open_file_dialog(
            initial_dir=DEFAULT_CONF_DIR, file_type=("YAML files", "*.yaml")
        )
        fabrication_conf.set_file(conf_file)
        logging.info("Configuration loaded from {}".format(conf_file))
    else:
        fabrication_conf.read(defaults=True, user=False)
        logging.info("Default configuration loaded from package")

    if not fabrication_conf["target"].exists():
        question = questionary.select(
            "Target?", choices=["Virtual robot", "Real robot"], default="Virtual robot"
        ).ask()
        fabrication_conf["target"] = "real" if question == "Real robot" else "virtual"

    logging.info(
        "Target is {} controller.".format(fabrication_conf["target"].get().upper())
    )

    # At this point the conf is considered set, if changes needs to happen after
    # this point CONF needs to be set again. There's probably a better way though.
    global CONF
    CONF = fabrication_conf.get(abb_rcf_conf_template)

    logging.info("Configuration \n{}".format(fabrication_conf.dump()))

    conf_ok = questionary.confirm("Configuration correct?").ask()
    if not conf_ok:
        logging.critical("Program exited because user didn't confirm config")
        print("Exiting.")
        sys.exit()


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
    index = index % (CONF.pick.xnum * CONF.pick.ynum)

    xpos = index % CONF.pick.xnum
    ypos = index // CONF.pick.xnum

    x = CONF.pick.origin_grid.x + xpos * CONF.pick.grid_spacing
    y = CONF.pick.origin_grid.y + ypos * CONF.pick.grid_spacing
    z = bullet_height * CONF.pick.compression_height_factor

    frame = Frame(Point(x, y, z), Vector(*CONF.pick.xaxis), Vector(*CONF.pick.yaxis))
    logging.debug("Picking frame {:03d}: {}".format(index, frame))
    return frame


################################################################################
# Script runner                                                                #
################################################################################
def abb_run(cmd_line_args):
    """Fabrication runner, sets conf, reads json input and runs fabrication process."""
    fabrication_conf.set_args(cmd_line_args)

    ############################################################################
    # Logging setup                                                            #
    ############################################################################
    timestamp_file = datetime.now().strftime("%Y%m%d-%H.%M_rcf_abb.log")
    log_file = DEFAULT_LOG_DIR / timestamp_file

    handlers = []

    if not fabrication_conf["skip_logfile"]:
        handlers.append(logging.FileHandler(log_file, mode="a"))

    if not fabrication_conf["quiet"]:
        handlers.append(logging.StreamHandler(sys.stdout))

    logging.basicConfig(
        level=logging.DEBUG if fabrication_conf["debug"] else logging.INFO,
        format="%(asctime)s:%(levelname)s:%(funcName)s:%(message)s",
        handlers=handlers,
    )

    logging.info("compas_rcf version: {}".format(__version__))
    logging.debug("argparse input: {}".format(cmd_line_args))
    logging.debug("config after set_args: {}".format(fabrication_conf))

    ############################################################################
    # CONF setup                                                              #
    ############################################################################
    get_settings()

    ############################################################################
    # Docker setup                                                            #
    ############################################################################
    compose_up(docker_compose_paths["base"], remove_orphans=False)
    logging.debug("Compose up base")
    ip = robot_ips[CONF.target]
    compose_up(docker_compose_paths["abb_driver"], ROBOT_IP=ip)
    logging.debug("Compose up abb_driver")

    ############################################################################
    # Load fabrication data                                                    #
    ############################################################################
    json_path = Path(ui.open_file_dialog(initial_dir=DEFAULT_JSON_DIR))

    clay_bullets = load_bullets(json_path)
    logging.info("Fabrication data read from: {}".format(json_path))
    logging.info("{} items in clay_bullets.".format(len(clay_bullets)))

    ############################################################################
    # Create Ros Client                                                        #
    ############################################################################
    ros = RosClient()

    ############################################################################
    # Create ABB Client                                                        #
    ############################################################################
    abb = AbbClient(ros)
    abb.run()
    logging.debug("Connected to ROS")

    ############################################################################
    # Connection check                                                         #
    ############################################################################
    ip = robot_ips[CONF.target]
    for i in range(3):
        try:
            logging.debug("Pinging robot")
            ping(abb, timeout=CONF.docker.timeout_ping)
            logging.debug("Breaking loop after successful ping")
            break
        except TimeoutError:
            logging.info("No response from controller, restarting abb-driver service.")
            compose_up(
                docker_compose_paths["abb_driver"], force_recreate=True, ROBOT_IP=ip
            )
            logging.debug("Compose up for abb_driver with robot-ip={}".format(ip))
            time.sleep(CONF.docker.sleep_after_up)
    else:
        raise TimeoutError("Failed to connect to robot")

    ############################################################################
    # Set speed, accel, tool, wobj and move to start pos                       #
    ############################################################################
    initial_setup(abb)

    ############################################################################
    # setup in_progress JSON                                                   #
    ############################################################################
    json_progress_identifier = "IN_PROGRESS-"

    if json_path.name.startswith(json_progress_identifier):
        in_progress_json = json_path
    else:
        in_progress_json = json_path.with_name(
            json_progress_identifier + json_path.name
        )

    ############################################################################
    # Check for placed bullets in JSON #
    ############################################################################

    maybe_placed = [bullet for bullet in clay_bullets if bullet.placed is not None]

    if len(maybe_placed) < 1:
        to_place = clay_bullets[:]
    else:
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
                    "Number of bullets to place again counted from last bullet",
                    "1",
                    lambda val: val.isdigit(),
                ).ask()
                last_placed = max(maybe_placed, key=attrgetter("bullet_id"))
                last_placed_index = clay_bullets.index(last_placed)
                to_place = clay_bullets[last_placed_index - int(n_place_again) + 1 :]
            else:
                to_place_selection = questionary.checkbox(
                    "Select bullets:",
                    [
                        "{} (id {}), marked placed: {}".format(
                            i, bullet.bullet_id, bullet.placed is not None
                        )
                        for i, bullet in enumerate(clay_bullets)
                    ],
                ).ask()
                indices = [int(bullet.split()[0]) for bullet in to_place_selection]
                to_place = [clay_bullets[i] for i in indices]

        for bullet in to_place:
            bullet.placed = None
            bullet.cycle_time = None

    ############################################################################
    # Fabrication loop                                                         #
    ############################################################################

    for i, bullet in enumerate(to_place):
        current_bullet_desc = "Bullet {:03d}/{:03d} with id {}".format(
            i + 1, len(to_place), bullet.bullet_id
        )

        abb.send(PrintText(current_bullet_desc))
        logging.info(current_bullet_desc)

        pick_frame = pick_frame_from_grid(i, bullet.height)

        # Pick bullet
        pick_future = send_picking(abb, pick_frame)

        # Place bullet
        place_future = send_placing(abb, bullet)

        # This both sets cycle_time and blocks script until robot finishes pick & place
        cycle_time = pick_future.result() + place_future.result()

        bullet.cycle_time = cycle_time
        logging.debug("Cycle time was {}".format(bullet.cycle_time))
        bullet.placed = time.time()
        logging.debug("Time placed was {}".format(bullet.placed))

        with in_progress_json.open(mode="w") as fp:
            json.dump(clay_bullets, fp, cls=ClayBulletEncoder)

    ############################################################################
    # Shutdown procedure                                                       #
    ############################################################################

    if len([bullet for bullet in clay_bullets if bullet.placed is None]) == 0:
        in_progress_json.unlink()  # Remove in progress json

        done_json = DEFAULT_JSON_DIR / "00_done" / json_path.name

        with done_json.open(mode="w") as fp:
            json.dump(clay_bullets, fp, cls=ClayBulletEncoder)

        logging.debug("Saved placed bullets to 00_Done.")
    else:
        logging.debug(
            "Bullets without placed timestamp still present, keeping {}".format(
                in_progress_json.name
            )
        )

    logging.info("Finished program with {} bullets.".format(len(to_place)))
    shutdown_procedure(abb)


if __name__ == "__main__":
    """Entry point and argument handling
    """
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

    args = parser.parse_args()

    abb_run(args)
