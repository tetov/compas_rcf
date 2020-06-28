"""Helpers for scripts interacting with ABB robots or RAPID code."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import time
from os.path import join

from compas_rrc import FeedbackLevel
from compas_rrc import Noop
from compas_rrc import TimeoutException

from compas_rcf import DOCKER_COMPOSE_DIR
from compas_rcf.docker import restart_container

__all__ = [
    "ZONE_DICT",
    "DOCKER_COMPOSE_PATHS",
    "DRIVER_CONTAINER_NAME",
    "ROBOT_IPS",
    "ping",
    "check_reconnect"
]

log = logging.getLogger(__name__)

# Describes the valid zone data definitions.
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
    "Z200": 200
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
    feedback = client.send(Noop(feedback_level=FeedbackLevel.DONE))

    return feedback.result(timeout=timeout)


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
