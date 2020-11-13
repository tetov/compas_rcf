from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import logging

import questionary
from compas_rrc import MoveToJoints
from compas_rrc import PrintText
from compas_rrc import RobotJoints
from compas_rrc import SetAcceleration
from compas_rrc import SetMaxSpeed
from compas_rrc import Zone

from rapid_clay_formations_fab.robots import AbbRcfClient
from rapid_clay_formations_fab.robots._scripts import compose_up_driver

log: logging.Logger = logging.getLogger(__name__)

CALIBRATION_JOINT_POSITION = RobotJoints(0, 0, 0, 0, 0, 0)
TRAVEL_JOINT_POSITION = RobotJoints(0, -87, 65, 0, 0, 0)

SPEED = 150
ZONE = Zone.FINE

ACCEL = 100
ACCEL_RAMP = 100
SPEED_OVERRIDE = 100
SPEED_MAX_TCP = 300


def go_to_joint_pos(args: argparse.Namespace) -> None:
    """Send instruction to go to joint position.

    Parameters
    ----------
    args : :class:`argparse.Namespace`
    """
    selection_instructions = {
        "Calibration position": CALIBRATION_JOINT_POSITION,
        "Travel position": TRAVEL_JOINT_POSITION,
    }

    compose_up_driver(args.controller)

    selection = questionary.select(
        "Select joint position to go to", selection_instructions.keys()
    ).ask()

    log.debug(f"{selection} selected.")

    with AbbRcfClient(ros_port=9090) as client:
        client.ensure_connection()

        client.send(SetAcceleration(ACCEL, ACCEL_RAMP))
        client.send(SetMaxSpeed(SPEED_OVERRIDE, SPEED_MAX_TCP))

        client.confirm_start()

        client.send(PrintText(f"Moving to {selection.lower()}."))

        client.send(
            MoveToJoints(
                selection_instructions[selection],
                client.EXTERNAL_AXES_DUMMY,
                SPEED,
                ZONE,
            )
        )
