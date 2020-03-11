from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import os
import subprocess
import sys

log = logging.getLogger(__name__)


def _setup_env_vars(env_vars):
    list_vars = []
    for key in env_vars:
        if os.name == "nt":
            list_vars.append("set")
        list_vars.append("{}={}".format(key.upper(), env_vars[key]))
        list_vars.append("&&")

    return list_vars


def _run(cmd, check_output=False, print_output=True, **kwargs):
    if sys.version_info.major < 3:
        if check_output:
            subprocess.check_call(cmd, universal_newlines=print_output, **kwargs)
        else:
            subprocess.call(cmd, universal_newlines=print_output, **kwargs)
    else:
        subprocess.run(cmd, check=check_output, text=print_output, **kwargs)


def compose_up(
    path,
    force_recreate=False,
    remove_orphans=False,
    ignore_orphans=True,
    print_output=True,
    check_output=True,
    env_vars={},
):

    run_kwargs = {}
    run_kwargs.update({"check_output": check_output})
    run_kwargs.update({"print_output": print_output})

    cmd = ["docker-compose", "--file", str(path), "up", "--detach"]

    log.debug("Env vars: {}".format(env_vars))

    if ignore_orphans:
        env_vars.update({"COMPOSE_IGNORE_ORPHANS": "true"})

    if len(env_vars) > 0:
        cmd = _setup_env_vars(env_vars) + cmd
        run_kwargs.update({"shell": True})

    if force_recreate:
        cmd.append("--force-recreate")

    if remove_orphans:
        cmd.append("--remove-orphans")

    log.debug("Command to run: {}".format(cmd))

    _run(cmd, **run_kwargs)


def compose_down(path):
    """Run ``docker-compose down`` for specified compose file.

    Parameters
    ----------
    path : pathlike object
        Path to compose file
    """
    cmd = ["docker-compose", "--file", str(path), "down"]

    _run(cmd)
