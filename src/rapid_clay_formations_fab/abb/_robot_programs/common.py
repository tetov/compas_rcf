"""Functions shared between robot programs."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging

from rapid_clay_formations_fab.abb import DOCKER_COMPOSE_PATHS
from rapid_clay_formations_fab.abb import ROBOT_IPS
from rapid_clay_formations_fab.docker import compose_up

log = logging.getLogger(__name__)


def compose_up_driver(target_controller):
    """Compose up ROS services for compas_rrc ABB controll.

    Parameters
    ----------
    target_controller : :obj:`str`
        Target key, either ``"real"`` or ``"virtual"``, used for dictionary
        of IPs used to connect to controller.
    """
    ip = {"ROBOT_IP": ROBOT_IPS[target_controller]}
    compose_up(DOCKER_COMPOSE_PATHS["driver"], check_output=True, env_vars=ip)
    log.debug("Driver services are running.")
