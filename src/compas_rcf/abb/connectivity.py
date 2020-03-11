"""Helpers for scripts interacting with ABB robots or RAPID code."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import time
from os.path import join
from sys import version_info

from compas_rrc import FeedbackLevel
from compas_rrc import Noop

from compas_rcf import HERE
from compas_rcf.docker import compose_up

if version_info.major > 2:
    from compas_rcf.fabrication.conf import FABRICATION_CONF as fab_conf

_path_from_pkg = ["docker", "compose_files", "abb"]
_compose_folder = join(HERE, *_path_from_pkg)
_base_name = "master-bridge-docker-compose.yml"
_driver_name = "abb-driver-docker-compose.yml"

DOCKER_COMPOSE_PATHS = {
    "base": join(_compose_folder, _base_name),
    "driver": join(_compose_folder, _driver_name),
}

ROBOT_IPS = {"real": "192.168.125.1", "virtual": "host.docker.internal"}


log = logging.getLogger(__name__)


def ping(client, timeout=10):
    feedback = client.send(Noop(feedback_level=FeedbackLevel.DONE))

    try:
        return feedback.result(timeout=timeout)
    except Exception as e:
        if e.args[0] == "Timeout: future result not available":
            raise TimeoutError(e.args)
        else:
            raise


def connection_check(client):
    """Check connection to ABB controller."""
    env_vars = {"ROBOT_IP": ROBOT_IPS[fab_conf["target"].as_str()]}
    for i in range(3):
        try:
            log.debug("Pinging robot")
            ping(client, timeout=fab_conf["docker"]["timeout_ping"].get())
            log.debug("Breaking loop after successful ping")
            break
        except TimeoutError:
            log.info("No response from controller, restarting abb-driver service.")
            compose_up(
                DOCKER_COMPOSE_PATHS["driver"], force_recreate=True, env_vars=env_vars,
            )
            log.debug(
                "Compose up for abb_driver with robot-ip={}".format(
                    env_vars["ROBOT_IP"]
                )
            )
            time.sleep(fab_conf["docker"]["sleep_after_up"].get())
    else:
        raise TimeoutError("Failed to connect to robot")
