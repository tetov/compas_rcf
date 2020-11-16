from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
from pathlib import Path

from compas.utilities import pairwise

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
            "If CTRL-C is not working properly, you might need to set "
            + f'environment variable {env_var_name} = "1" before running the script.'
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


def rotate_files(
    file_path: Path, max_size_mb: float = 10, max_n_logs: int = None
) -> None:
    """Rotate files if the given file is too large.

    Parameters
    ----------
    file_path
        Path to the file that might need to be rotated.
    max_size_mb
        Max size of file in MB before rotation.
    max_n_logs
        Max number of files to keep.
    """
    if file_path.stat().st_size < max_size_mb * 1e6:
        return

    to_keep = []

    i = 0
    existing_files = [f for f in file_path.parent.iterdir() if file_path.name in f.stem]
    existing_files.sort()
    for file_ in existing_files:
        if max_n_logs and i > max_n_logs:
            break

        to_keep.append(file_)
        i += 1

    last_file = file_path.with_name(file_path.name + f".{i:02}")

    files_ = to_keep + [last_file]

    for older, newer in pairwise(reversed(files_)):
        newer.replace(older)
