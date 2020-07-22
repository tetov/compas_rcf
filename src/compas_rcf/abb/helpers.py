"""Helpers for scripts interacting with ABB robots or RAPID code."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import time
from collections import Sequence
from os.path import join

from compas_fab.backends import RosClient
from compas_rrc import AbbClient
from compas_rrc import FeedbackLevel
from compas_rrc import Motion
from compas_rrc import MoveToFrame
from compas_rrc import Noop
from compas_rrc import PrintText
from compas_rrc import SetAcceleration
from compas_rrc import SetMaxSpeed
from compas_rrc import SetTool
from compas_rrc import SetWorkObject
from compas_rrc import TimeoutException
from compas_rrc import Zone

from compas_rcf import DOCKER_COMPOSE_DIR
from compas_rcf.docker import restart_container

log = logging.getLogger(__name__)

# Describes the valid zone data definitions.
# Used in confuse conf file
ZONE_DICT = {
    "FINE": -1,
    "Z0": 0,
    "Z1": 1,
    "Z5": 5,
    "Z10": 10,
    "Z15": 15,
    "Z20": 20,
    "Z30": 30,
    "Z40": 40,
    "Z50": 50,
    "Z60": 60,
    "Z80": 80,
    "Z100": 100,
    "Z150": 150,
    "Z200": 200,
}

_compose_file_name = "docker-compose.yml"
_driver_compose_dir = "abb-driver"
_planner_compose_dir = "abb-planner"

DOCKER_COMPOSE_PATHS = {
    "driver": join(DOCKER_COMPOSE_DIR, _driver_compose_dir, _compose_file_name),
    "planner": join(DOCKER_COMPOSE_DIR, _planner_compose_dir, _compose_file_name),
}

DRIVER_CONTAINER_NAME = "abb-driver"

ROBOT_IPS = {"real": "192.168.125.1", "virtual": "host.docker.internal"}


def ping(client, timeout=10):
    """Ping ABB robot controller.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
        Client connected to controller.
    timeout : :class:`float`, optional
        Timeout for reply. Defaults to ``10``.

    Raises
    ------
    :exc:`TimeoutError`
        If no reply is returned before timeout.
    """
    client.send_and_wait(Noop(feedback_level=FeedbackLevel.DONE), timeout=timeout)


def check_reconnect(
    client, driver_container_name="abb-driver", timeout_ping=5, wait_after_up=2, tries=3
):
    """Check connection to ABB controller and restart abb-driver if necessary.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
        Client connected to controller.
    timeout_ping : :class:`float`, optional
        Timeout for ping response.
    wait_after_up : :class:`float`, optional
        Time to wait to ping after `abb-driver` container started.

    Raises
    ------
    :exc:`TimeoutError`
        If no reply is returned before timeout.
    """
    for _ in range(tries):
        try:
            log.debug("Pinging robot")
            ping(client, timeout_ping)
            log.debug("Breaking loop after successful ping.")
            break
        except TimeoutException:
            log.info("No response from controller, restarting abb-driver service.")
            restart_container(driver_container_name)
            time.sleep(wait_after_up)
    else:
        raise TimeoutException("Failed to connect to robot.")


def std_move_to_frame(
    frame,
    tool="tool0",
    wobj="wobj0",
    motion_type=Motion.LINEAR,
    speed=200,
    accel=100,
    zone=Zone.FINE,
    timeout=None,
):
    """Move robot arm to target or targets.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame` or :obj:`list` of :class:`compas.geometry.Frame`
        Target frame or frames.
    tool : :obj:`str`
        Name of tool as named in RAPID code on controller to use for TCP data.
    wobj : :obj:`str`
        Name of work object as named in RAPID code on controller to use for
        coordinate system.
    motion_type : :class:`compas_rrc.Motion`
        Motion type, either linear (:class:`~compas_rrc.Motion.LINEAR`) or
        joint (:class:`~compas_rrc.Motion.JOINT`).
    speed : :obj:`float`
        TCP speed in mm/s. Limited by hard coded max speed in this function as
        well as safety systems on controller.
    accel : :obj:`float`
        Acceleration in percentage of standard acceleration.
    zone : :class:`compas_rrc.Zone`
        Set zone value of movement, (acceptable deviation from target).
    timeout : :obj:`float`
        Time to wait for indication of finished movement. If not defined no
        feedback will be requested.
    """  # noqa: E501
    if not isinstance(frame, Sequence):
        frames = [frame]
    else:
        frames = frame

    with RosClient() as ros:
        # Create ABB Client
        abb = AbbClient(ros)
        abb.run(timeout=5)

        abb.send(SetTool(tool))
        abb.send(SetWorkObject(wobj))

        # Set acceleration data
        ramp = 100  # % Higher values makes the acceleration ramp longer
        abb.send(SetAcceleration(accel, ramp))

        # Set speed override and max speed
        speed_override = 100  # %
        max_tcp_speed = 500  # mm/s
        abb.send(SetMaxSpeed(speed_override, max_tcp_speed))

        # Move to Frame
        for f in frames:
            abb.send(
                PrintText(" Moving to {:.3f}, {:.3f}, {:.3f}.".format(*f.point.data))
            )
            abb.send(MoveToFrame(f, speed, zone, motion_type))

        if timeout:
            abb.send_and_wait(Noop(), timeout=timeout)
