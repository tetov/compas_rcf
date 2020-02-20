"""Helpers for scripts interacting with ABB robots or RAPID code."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_rrc import Noop
from compas_rrc import FeedbackLevel

from compas_rcf import HERE

# Describes the valid zone data definitions.
zone_dict = {
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

try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path

pkg_dir = Path(HERE)

_compose_folder = pkg_dir / "utils" / "docker" / "compose_files" / "abb"
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
