"""Helpers for scripts interacting with ABB robots or RAPID code."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import time
from pathlib import Path

from compas_rrc import FeedbackLevel
from compas_rrc import Noop

from compas_rcf import HERE
from compas_rcf.docker import compose_up
from compas_rcf.fabrication.conf import FABRICATION_CONF as fab_conf

pkg_dir = Path(HERE)

_compose_folder = pkg_dir / "docker" / "compose_files" / "abb"
DOCKER_COMPOSE_PATHS = {
    "base": _compose_folder / "master-bridge-docker-compose.yml",
    "driver": _compose_folder / "abb-driver-docker-compose.yml",
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
