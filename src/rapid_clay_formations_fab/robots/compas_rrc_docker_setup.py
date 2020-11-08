"""Docker setup for compas_rrc_driver."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from os.path import join

from rapid_clay_formations_fab import DOCKER_COMPOSE_DIR

_compose_file_name = "docker-compose.yml"
_driver_compose_dir = "abb-driver"
_planner_compose_dir = "abb-planner"

DOCKER_COMPOSE_PATHS = {
    "driver": join(DOCKER_COMPOSE_DIR, _driver_compose_dir, _compose_file_name),
    "planner": join(DOCKER_COMPOSE_DIR, _planner_compose_dir, _compose_file_name),
}

DRIVER_CONTAINER_NAME = "abb-driver"
DRIVER_IMAGE_NAME = "tetov/compas_rrc_driver:1.0.0"

ROBOT_IPS = {"real": "192.168.125.1", "virtual": "host.docker.internal"}
