from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from subprocess import run

RUN_KWARGS = {
    "check": True,
    # "capture_output": True,
    # "stdout": subprocess.PIPE,
    # "stderr": subprocess.STDOUT,
    "text": True,
    # "encoding": 'utf-8',
    # "universal_newlines": True
}


def setup_env_vars(env_vars):
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

    if ignore_orphans:
        env_vars.update({"COMPOSE_IGNORE_ORPHANS": "true"})

    if len(env_vars) > 0:
        cmd = setup_env_vars(env_vars) + cmd
        shell = True
    else:
        shell = False

    if force_recreate:
        cmd.append("--force-recreate")

    if remove_orphans:
        cmd.append("--remove-orphans")

    run(cmd, shell=shell, **RUN_KWARGS)


def compose_run(path, **env_vars):
    cmd = ["docker-compose", "--file", str(path), "run", "--detach"]

    if len(env_vars) > 0:
        cmd = setup_env_vars(env_vars) + cmd
        shell = True
    else:
        shell = False

    run(cmd, shell=shell, **RUN_KWARGS)


def compose_down(path):
    cmd = ["docker-compose", "--file", str(path), "down"]
    run(cmd, **RUN_KWARGS)
    cmd_post = ["docker-compose", "--file", str(path), "rm"]
    run(cmd_post, **RUN_KWARGS)


def compose_restart(path, **env_vars):

    cmd = ["docker-compose", "--file", str(path), "restart"]

    if len(env_vars) > 0:
        cmd = setup_env_vars(env_vars) + cmd
        shell = True
    else:
        shell = False

    run(cmd, shell=shell, **RUN_KWARGS)


def container_restart(container_name):
    return run("docker restart {}".format(container_name), **RUN_KWARGS)
