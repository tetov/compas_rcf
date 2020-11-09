from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os

from rapid_clay_formations_fab.docker import compose_up
from rapid_clay_formations_fab.robots import DOCKER_COMPOSE_PATHS
from rapid_clay_formations_fab.robots import ROBOT_IPS

log = logging.getLogger(__name__)


def warn_about_scipy_fortran_ctrl_c() -> None:
    """Warn about potential problem with CTRL-C catching.

    See https://github.com/ContinuumIO/anaconda-issues/issues/905#issuecomment-232498034
    """
    env_var_name = "FOR_DISABLE_CONSOLE_CTRL_HANDLER"
    if not os.environ.get(env_var_name):
        log.warning(
            f'If CTRL-C is not working properly, you might need to set environment variable {env_var_name} = "1" before running the script.'  # noqa: E501
        )


def compose_up_driver(target_controller: str):
    """Compose up ROS application for compas_rrc ABB driver.

    Parameters
    ----------
    target_controller
        Target key, either ``"real"`` or ``"virtual"``, used as key for
        dictionary of controller IPs.
    """
    ip = {"ROBOT_IP": ROBOT_IPS[target_controller]}
    compose_up(DOCKER_COMPOSE_PATHS["driver"], check_output=True, env_vars=ip)
    log.debug("Driver application is running.")
