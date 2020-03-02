from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from subprocess import run
import logging

log = logging.getLogger(__name__)


RUN_KWARGS = {
    "check": True,
    # "capture_output": True,
    # "stdout": subprocess.PIPE,
    # "stderr": subprocess.STDOUT,
    "text": True,
    # "encoding": 'utf-8',
    # "universal_newlines": True
}


def _setup_env_vars(env_vars):
    list_vars = []
    for key in env_vars:
        if os.name == "nt":
            list_vars.append("set")
        list_vars.append("{}={}".format(key.upper(), env_vars[key]))
        list_vars.append("&&")

    return list_vars


def compose_up(
    path, force_recreate=False, remove_orphans=False, ignore_orphans=True, **env_vars
):
    cmd = ["docker-compose", "--file", str(path), "up", "--detach"]

    log.debug("Env vars: {}".format(env_vars))

    if ignore_orphans:
        env_vars.update({"COMPOSE_IGNORE_ORPHANS": "true"})

    if len(env_vars) > 0:
        cmd = _setup_env_vars(env_vars) + cmd
        shell = True
    else:
        shell = False

    if force_recreate:
        cmd.append("--force-recreate")

    if remove_orphans:
        cmd.append("--remove-orphans")

    log.debug("Command to run: {}".format(cmd))

    run(cmd, shell=shell, **RUN_KWARGS)
