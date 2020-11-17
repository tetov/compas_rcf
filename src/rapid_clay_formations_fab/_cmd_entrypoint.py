"""Fabrication runner entrypoint.

Run from command line using :code:`rcf_run`
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import json
import logging
import pathlib
import typing
from datetime import datetime

import confuse
from compas.rpc.services.default import start_service as start_rpc_service
from compas.utilities import DataDecoder

import rapid_clay_formations_fab.robots._scripts as scripts
from rapid_clay_formations_fab import __version__
from rapid_clay_formations_fab.fab_data import ABB_RCF_CONF_TEMPLATE
from rapid_clay_formations_fab.fab_data import fab_conf
from rapid_clay_formations_fab.rhino.install import install_pkgs_to_rhino


def main() -> None:
    """Entry point, logging setup and argument handling."""

    # TODO: Add install and proxy
    parser = argparse.ArgumentParser()

    # Controller setting
    parser.add_argument(
        "-c",
        "--controller",
        choices=["real", "virtual"],
        default="virtual",
        help="Set script target.",
    )

    # Loglevel settings
    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show DEBUG level log messages.",
    )
    group.add_argument(
        "-q", "--quiet", action="store_true", help="Supress log messages."
    )

    # Subparsers / scripts
    subparsers = parser.add_subparsers(title="Scripts")
    parser_fab = subparsers.add_parser(
        "fabrication", aliases=["fab"], help="Fabrication script."
    )
    parser_fab.set_defaults(func=_fab_entrypoint)

    parser_rec = subparsers.add_parser(
        "record_poses", aliases=["rec", "record"], help="Record poses for localization."
    )
    parser_rec.set_defaults(func=scripts.record_poses)

    parser_goto = subparsers.add_parser(
        "go_to_joint_pos", aliases=["goto"], help="Go to joint pose."
    )
    parser_goto.set_defaults(func=scripts.go_to_joint_pos)

    parser_rhino_install = subparsers.add_parser(
        "rhino_install",
        aliases=["install"],
        help="Install packages to Rhino python environment.",
    )
    parser_rhino_install.set_defaults(func=install_pkgs_to_rhino)

    parser_proxy = subparsers.add_parser(
        "proxy", aliases=["rpc"], help="Start a compas rpc proxy on port 12457."
    )
    parser_proxy.set_defaults(func=_rpc_entrypoint)

    # fab specific
    parser_fab.add_argument(
        "run_data_path",
        type=pathlib.Path,
        help="File containing fabrication setup.",
    )

    parser_test = subparsers.add_parser(
        "test", aliases=["test"], help="Run integration test."
    )
    parser_test.set_defaults(func=_test_entrypoint)
    # fab specific
    parser_test.add_argument(
        "run_data_path",
        type=pathlib.Path,
        help="File containing fabrication setup.",
    )

    # fab specific
    args = parser.parse_args()

    _setup_logger(args)

    # Run function defined as default for each subparser.
    args.func(args)


def _rpc_entrypoint(*args):
    start_rpc_service(12457)


def _fab_entrypoint(args: argparse.Namespace) -> None:
    log = logging.getLogger(__name__)

    run_data = _load_rundata(args.run_data_path)

    run_conf = _setup_run_conf(args, run_data)

    _setup_file_logger(run_data["log_dir"])

    log.info(f"rapid_clay_formations_fab version: {__version__}")
    log.info(f"Using {run_conf.robot_client.controller} controller.")
    log.debug(f"argparse input: {args}")
    log.debug(f"config after set_args: {fab_conf}")

    scripts.fabrication(run_conf, run_data)


def _test_entrypoint(args):

    run_data = _load_rundata(args.run_data_path)
    run_conf = _setup_run_conf(args, run_data)

    scripts.test_speeds(run_conf, run_data)


def _load_rundata(run_data_path: pathlib.Path) -> typing.Any:
    # Load dictionary from file specified on command line
    with run_data_path.open(mode="r") as f:
        run_data = json.load(f, cls=DataDecoder)
    return typing.cast(dict, run_data)  # cast does not change or check during runtime


def _setup_file_logger(log_dir: typing.Union[pathlib.Path, str]) -> None:
    log = logging.getLogger(__name__)

    # cast to path obj
    log_dir = pathlib.Path(log_dir)

    # 1 logfile per run, named with a timestamp
    timestamp_logfile = datetime.now().strftime("%Y%m%d-%H.%M.%S.log")
    log_file = log_dir / timestamp_logfile

    log.addHandler(logging.FileHandler(log_file, mode="a"))


def _setup_run_conf(args: argparse.Namespace, run_data: dict) -> confuse.AttrDict:
    log = logging.getLogger(__name__)

    # Read config-default.yml for default values
    fab_conf.read(user=False, defaults=True)

    # Read conf file specified in run_data
    fab_conf.set_file(run_data["conf_path"])
    log.info(f"Configuration loaded from {run_data['conf_path']}")

    # Move controller setting to be under robot_client in conf
    fab_conf["robot_client"]["controller"] = args.controller

    # Clean args a bit since whole namespace will be checked by confuse
    unwanted_args = ("quiet", "verbose", "func", "controller")
    for arg in unwanted_args:
        if arg in args:
            delattr(args, arg)

    # Import options from argparse
    fab_conf.set_args(args)

    # Validate conf
    run_conf = fab_conf.get(ABB_RCF_CONF_TEMPLATE)

    return run_conf


def _setup_logger(args: argparse.Namespace) -> None:
    """Configure logging from command line arguments."""

    if args.verbose:
        loglevel = logging.DEBUG
    elif args.quiet:
        loglevel = logging.WARN
    else:
        loglevel = logging.INFO

    logging.basicConfig(
        level=loglevel,
        format="%(asctime)s:%(levelname)s:%(funcName)s:%(message)s",
    )


if __name__ == "__main__":
    main()
