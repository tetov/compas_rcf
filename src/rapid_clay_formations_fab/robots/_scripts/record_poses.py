"""Program recording poses for localization procedure."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import json
import logging
import time
import typing
from datetime import datetime
from pathlib import Path

import compas
import compas_rrc

from rapid_clay_formations_fab.robots import AbbRcfClient
from rapid_clay_formations_fab.robots import PrintTextNoErase
from rapid_clay_formations_fab.robots import StopAll
from rapid_clay_formations_fab.robots._scripts import compose_up_driver
from rapid_clay_formations_fab.robots._scripts import warn_about_scipy_fortran_ctrl_c

log: logging.Logger = logging.getLogger(__name__)

# NOTE: If ctrl+c does not abort cleanly, set the env variable to
# FOR_DISABLE_CONSOLE_CTRL_HANDLER=1

OUTPUT_DIR = Path(r"C:\rcf_robotcontrol\06_localization\01_frames_from_script")
# OUTPUT_DIR = Path("/home/tetov/")

STRFTIME_FMT = "%Y-%m-%dT%H.%M.%S"


def record_poses(args: argparse.Namespace) -> None:
    """Program recording poses for localization procedure."""
    log.info("Move to robot when prompted, press play on the pendant to record.")

    log.info("Press CTRL+C when you are done.")
    warn_about_scipy_fortran_ctrl_c()

    log.info("Starting ROS ABB Driver")

    compose_up_driver(args.controller)

    poses: typing.List[compas.geometry.Frame] = []

    file_name = datetime.now().strftime(STRFTIME_FMT) + ".json"
    output_file = OUTPUT_DIR / file_name
    output_file.touch()

    with AbbRcfClient() as client:

        client.send(compas_rrc.SetTool("t_A057_ClayTool02_Prism"))
        client.send(compas_rrc.SetWorkObject("wobj0"))

        client.check_reconnect()

        while True:
            client.send(
                PrintTextNoErase(f"Move robot to localization point {len(poses)+1}")
            )
            client.send(PrintTextNoErase("Press play to record position."))
            client.send(StopAll())
            pose_future = client.send(compas_rrc.GetFrame())

            try:
                # Wait for result
                # Sleeping allows catching KeyboardInterrupt
                while pose_future.done is False:
                    time.sleep(3)

            except KeyboardInterrupt:
                log.info("Exiting script.")
                break

            pose = pose_future.result()

            if pose in poses:
                error_msg = "Position already recorded."
                client.send(PrintTextNoErase(error_msg))
                log.warning(error_msg)
                continue

            poses.append(pose)
            log.info(f"Pose {len(poses)} recorded.")

            # Write on every loop for safety
            with output_file.open(mode="w") as fp:
                json.dump(poses, fp, cls=compas.utilities.DataEncoder)

            log.debug(f"Saved frames to {output_file}")
            client.send(PrintTextNoErase(f"Position {len(poses)} recorded."))
