"""Helpers for scripts interacting with ABB robots or RAPID code."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import time

from compas_rrc import FeedbackLevel
from compas_rrc import Noop

from compas_rcf import HERE
from compas_rcf.docker import compose_up
from compas_rcf.fabrication.conf import FABRICATION_CONF as fab_conf


try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

log = logging.getLogger(__name__)

pkg_dir = Path(HERE)

_compose_folder = pkg_dir / "docker" / "compose_files" / "abb"
docker_compose_paths = {
    "base": _compose_folder / "base-docker-compose.yml",
    "abb_driver": _compose_folder / "abb-driver-docker-compose.yml",
}
robot_ips = {"real": "192.168.125.1", "virtual": "host.docker.internal"}


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
    """Connection check."""
    ip = robot_ips[fab_conf["target"].get()]
    for i in range(3):
        try:
            log.debug("Pinging robot")
            ping(client, timeout=fab_conf["docker"]["timeout_ping"].get())
            log.debug("Breaking loop after successful ping")
            break
        except TimeoutError:
            log.info("No response from controller, restarting abb-driver service.")
            compose_up(
                docker_compose_paths["abb_driver"], force_recreate=True, ROBOT_IP=ip
            )
            log.debug("Compose up for abb_driver with robot-ip={}".format(ip))
            time.sleep(fab_conf["docker"]["sleep_after_up"].get())
    else:
        raise TimeoutError("Failed to connect to robot")
