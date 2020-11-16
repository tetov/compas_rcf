"""Speed test for RCF fabrication process.

Invoked by
``python -m rapid_clay_formations_fab.robots._script.test_speeds_wo_pick``.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

import compas_rrc
from compas.geometry import Frame
from compas_fab.backends.ros import RosClient
from compas_rrc import Motion
from compas_rrc import MoveToFrame
from compas_rrc import MoveToJoints
from compas_rrc import PrintText
from compas_rrc import RobotJoints
from compas_rrc import Zone

log = logging.getLogger(__name__)

TIMEOUT = None

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


def test_speeds():
    with RosClient() as ros:
        client = compas_rrc.AbbClient(ros)
        client.run()

        # Confirm start on flexpendant
        client.send(PrintText("Confirm start by pressing play."))
        client.send(compas_rrc.Stop())

        # The speed and acceleration values are then overriden here
        client.send(compas_rrc.SetMaxSpeed(SPEED_OVERRIDE, SPEED_MAX_TCP))
        client.send(compas_rrc.SetAcceleration(ACCELERATION, ACCELERATION_RAMP))
        client.send(PrintText(f"Speed override: {SPEED_OVERRIDE} %"))
        client.send(PrintText(f"Max TCP speed: {SPEED_OVERRIDE} mm/s"))
        client.send(PrintText(f"Acceleration: {ACCELERATION} %"))
        client.send(PrintText(f"Acceleration ramp: {ACCELERATION_RAMP} %"))

        client.send(compas_rrc.SetTool(client.pick_place_tool.name))
        client.send(compas_rrc.SetWorkObject("wobj0"))
        client.send(PrintText(f"Tool: {TOOL}"))
        client.send(PrintText(f"wobj: {WOBJ}"))

        if TEST_JOINT_POS:
            for i in range(N_TIMES_REPEAT_LISTS):
                speed = START_SPEED + SPEED_INCREMENTS * i
                client.send(
                    PrintText(
                        f"Speed: {speed} mm/s, Zone: {ZONE} mm.",
                    )
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
                client.send(PrintText(f"Cycle took {cycle_time} s."))

        if TEST_FRAMES:
            for i in range(N_TIMES_REPEAT_LISTS):
                speed = START_SPEED + SPEED_INCREMENTS * i
                client.send(
                    PrintText(
                        f"Speed: {speed} mm/s, Zone: {ZONE} mm.",
                    )
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
                client.send(PrintText(f"Cycle took {cycle_time} s."))

        client.close()


if __name__ == "__main__":
    test_speeds()
