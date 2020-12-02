"""
******************************************************************************
rapid_clay_formations_fab.docker
******************************************************************************

.. currentmodule:: rapid_clay_formations_fab.docker

Docker compose commands to be used from python scripts.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    compose_up
    compose_down
    restart_container
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import shlex
import subprocess
import sys
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import docker

log = logging.getLogger(__name__)


def compose_up(
    path: os.PathLike,
    overrides: List[os.PathLike] = None,
    force_recreate: bool = False,
    remove_orphans: bool = False,
    ignore_orphans: bool = True,
    quiet: bool = False,
    check: bool = True,
    additional_env_vars: dict = None,
) -> subprocess.CompletedProcess:
    """Run ``docker-compose up`` for specified compose file.

    Parameters
    ----------
    path
        Path to compose file.
    overrides
        List of docker-compose override files, e.g.
        ``docker-compose.override.yml``.
    force_recreate
        Force recreation of containers specified in ``docker-compose`` file.
        Defaults to ``False``.
    remove_orphans
        Remove orphaned containers. Defaults to ``False``.
    ignore_orphans
        Don't warn about orphaned containers (useful since the use of multiple
        compose files produces false positives for this check). Defaults to
        ``True``.
    quiet
        Suppress ``stdout`` and only print ``stderr``.
        Defaults to ``False``.
    check
        Raise if ``docker-compose`` fails. Defaults to ``True``.
    additional_env_vars
        Environment variables to set before running ``docker-compose``
    """
    env_vars = additional_env_vars or {}

    run_kwargs_type = Dict[str, Union[Optional[int], Optional[bool]]]

    run_kwargs: run_kwargs_type = {
        "check": check,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.STDOUT,
    }

    if quiet:
        run_kwargs["stdout"] = None
        run_kwargs["stderr"] = subprocess.PIPE

    paths = [path]
    if overrides:
        paths += overrides

    file_args = ""
    for path in paths:
        file_args += f"--file {path} "

    cmd_str = f"docker-compose {file_args} up --detach"
    cmd = shlex.split(cmd_str, posix="win" not in sys.platform)
    log.debug(f"Env vars: {env_vars}")

    if ignore_orphans:
        env_vars["COMPOSE_IGNORE_ORPHANS"] = "true"

    if force_recreate:
        cmd.append("--force-recreate")

    if remove_orphans:
        cmd.append("--remove-orphans")

    log.debug(f"Command to run: {cmd}")

    return subprocess.run(cmd, env=env_vars, **run_kwargs)  # type: ignore


def restart_container(name: str) -> None:
    d = docker.client.from_env()

    container = d.containers.get(name)
    container.restart()

    d.close()
