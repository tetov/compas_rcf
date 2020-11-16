"""Speed test for RCF fabrication process.

Invoked by ``rcf -c real test /path/to/test_run_data.json``. Only pick station
and configuration is read from the run_data file.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

import compas_rrc
from compas.geometry import Frame
from compas_rrc import Motion
from compas_rrc import MoveToFrame
from compas_rrc import MoveToJoints
from compas_rrc import RobotJoints
from compas_rrc import Zone

from rapid_clay_formations_fab.robots import AbbRcfFabricationClient
from rapid_clay_formations_fab.robots._scripts import compose_up_driver

log = logging.getLogger(__name__)

TIMEOUT = None

PICK_ELEMENT = True

TOOL = "t_A057_ClayTool02"
WOBJ = "wobj0"

SPEED_MAX_TCP = 250
SPEED_OVERRIDE = 100

ACCELERATION = 100
ACCELERATION_RAMP = 100

START_SPEED = 250
SPEED_INCREMENTS = 50

ZONE = Zone.Z100

MOTION_TYPE = Motion.JOINT  # Motion.LINEAR or Motion.JOINT

TEST_FRAMES = True
TEST_JOINT_POS = True

FRAMES = [
    Frame([-1000, -1250, 500], [0, -1, 0], [-1, 0, 0]),
    Frame([0, -1400, 1000], [1, 0, 0], [0, -1, 0]),
    Frame([1250, -1000, 500], [0, 1, 0], [1, 0, 0]),
    Frame([-500, -1000, 750], [0, 1, 0], [1, 0, 0]),
]

JOINT_POS = [
    RobotJoints(-81, -24, 55, 7, 69, 0),
    RobotJoints(-98, -2, 43, 0, 53, 0),
    RobotJoints(-19, 19, 40, 0, 30, 0),
]

N_TIMES_REPEAT_LISTS = 3


def test_speeds(run_conf, run_data):
    rob_conf = run_conf.robot_client

    # Compose up master, driver, bridge
    compose_up_driver(rob_conf.controller)

    pick_station = run_data["pick_station"]

    # This context manager sets up RosClient, inherits from AbbClient
    # with added fabrication specific methods
    # On exit it unadvertises topics and stops RosClient
    with AbbRcfFabricationClient(rob_conf, pick_station) as client:
        # Sends ping (noop) and restarts container if no response
        client.ensure_connection()

        client.log_and_print("Confirm start by pressing play.")
        # Confirm start on flexpendant
        client.confirm_start()

        # Sends move to start position, retracts needles and sets the defaults
        # speed and acceleration values.
        client.pre_procedure()

        # The speed and acceleration values are then overriden here
        client.send(compas_rrc.SetMaxSpeed(SPEED_OVERRIDE, SPEED_MAX_TCP))
        client.send(compas_rrc.SetAcceleration(ACCELERATION, ACCELERATION_RAMP))
        client.log_and_print(f"Speed override: {SPEED_OVERRIDE} %")
        client.log_and_print(f"Max TCP speed: {SPEED_OVERRIDE} mm/s")
        client.log_and_print(f"Acceleration: {ACCELERATION} %")
        client.log_and_print(f"Acceleration ramp: {ACCELERATION_RAMP} %")

        if PICK_ELEMENT:
            # Sends instruction to pick up element from first position
            # Subsequent calls picks up from next positions
            client.pick_element()

        client.send(compas_rrc.SetTool(client.pick_place_tool.name))
        client.send(compas_rrc.SetWorkObject("wobj0"))
        client.log_and_print(f"Tool: {TOOL}")
        client.log_and_print(f"wobj: {WOBJ}")

        if TEST_FRAMES:
            for i in range(N_TIMES_REPEAT_LISTS):
                speed = START_SPEED + SPEED_INCREMENTS * i
                client.log_and_print(
                    f"Speed: {speed} mm/s, Zone: {ZONE} mm.",
                )

                client.send(compas_rrc.StartWatch())
                for frame in FRAMES:
                    client.send(
                        MoveToFrame(
                            frame,
                            speed,
                            ZONE,
                            motion_type=MOTION_TYPE,
                        )
                    )

                # Block until finished and print cycle time
                client.send(compas_rrc.StopWatch())
                cycle_time = client.send_and_wait(
                    compas_rrc.ReadWatch(), timeout=TIMEOUT
                )
                client.log_and_print(f"Cycle took {cycle_time} s.")

        if TEST_JOINT_POS:
            for i in range(N_TIMES_REPEAT_LISTS):
                speed = START_SPEED + SPEED_INCREMENTS * i
                client.log_and_print(
                    f"Speed: {speed} mm/s, Zone: {ZONE} mm.",
                )

                client.send(compas_rrc.StartWatch())
                for pos in JOINT_POS:
                    client.send(
                        MoveToJoints(pos, client.EXTERNAL_AXES_DUMMY, speed, ZONE)
                    )

                # Block until finished and print cycle time
                client.send(compas_rrc.StopWatch())
                cycle_time = client.send_and_wait(
                    compas_rrc.ReadWatch(), timeout=TIMEOUT
                )
                client.log_and_print(f"Cycle took {cycle_time} s.")
