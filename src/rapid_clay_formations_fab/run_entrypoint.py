"""Fabrication runner entrypoint.

Run from command line using :code:`rcf_run`
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import logging as log
import pathlib
import sys
from datetime import datetime
from pathlib import Path

from rapid_clay_formations_fab import __version__
from rapid_clay_formations_fab.abb import fab_run
from rapid_clay_formations_fab.fab_data import ABB_RCF_CONF_TEMPLATE
from rapid_clay_formations_fab.fab_data import fab_conf


def main():
    """Entry point, logging setup and argument handling."""
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Set log level. -v adds INFO messages and -vv adds DEBUG messages.",
    )
    parser.add_argument(
        "run_data_path",
        type=pathlib.Path,
        help="File containing fabrication setup.",
    )
    parser.add_argument(
        "-c",
        "--controller",
        choices=["real", "virtual"],
        default="virtual",
        dest="robot_client.controller",
        help="Set fabrication runner target.",
    )
    parser.add_argument(
        "--edit-sequence",
        "-e",
        action="store_true",
        dest="edit_sequence",
        help="Select cylinders to place or start index.",
    )
    args = parser.parse_args()

    # Load dictionary from file specified on command line
    with args.run_data_path.open(mode="r") as f:
        run_data = json.load(f)

    logging_setup(run_data["log_dir"], args.verbose)

    # Read config-default.yml for default values
    fab_conf.read(user=False, defaults=True)

    # Read conf file specified in run_data
    fab_conf.set_file(run_data["conf_path"])
    log.info(f"Configuration loaded from {run_data['conf_path']}")

    # Import options from argparse
    fab_conf.set_args(args, dots=True)

    fab_conf["pick_conf"] = run_data["pick_conf_path"]

    # Validate conf
    run_conf = fab_conf.get(ABB_RCF_CONF_TEMPLATE)

    log.info(f"rapid_clay_formations_fab version: {__version__}")
    log.info(f"Using {run_conf.robot_client.controller} controller.")
    log.debug(f"argparse input: {args}")
    log.debug(f"config after set_args: {fab_conf}")

    fab_run(run_conf, run_data)


def logging_setup(log_dir, log_level):
    """Configure logging for module and imported modules."""
    loglevel_dict = {0: log.WARNING, 1: log.INFO, 2: log.DEBUG}

    timestamp_file = datetime.now().strftime("%Y%m%d-%H.%M.%S.log")
    log_file = Path(log_dir) / timestamp_file

    log.basicConfig(
        level=loglevel_dict[log_level],
        format="%(asctime)s:%(levelname)s:%(funcName)s:%(message)s",
        handlers=[log.FileHandler(log_file, mode="a"), log.StreamHandler(sys.stdout)],
    )


if __name__ == "__main__":
    main()
