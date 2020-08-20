from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import logging

from compas_fab.backends.ros import RosClient
from compas_rrc import PrintText

from compas_rcf.abb import AbbRcfClient
from compas_rcf.fab_data import ClayBullet
from compas_rcf.utils import CompasObjEncoder
from compas_rcf.abb._robot_programs import compose_up_driver
from compas_rcf.abb._robot_programs import confirm_start

log = logging.getLogger(__name__)


def measure_run(run_conf, run_data):

    compose_up_driver(run_conf.robot_client.controller)

    clay_cylinders = [ClayBullet.from_data(data) for data in run_data["fab_data"]]

    log.info("Fabrication data read.")

    log.info(f"{len(clay_cylinders)} items in clay_cylinders.")

    run_data_path = run_conf.run_data_path

    output_path = run_data_path.with_name(
        run_data_path.stem + "-MEASURED" + run_data_path.suffix
    )

    with RosClient() as ros:

        rob_client = AbbRcfClient(ros, run_conf.robot_client)

        rob_client.check_reconnect()

        confirm_start()

        # Set speed, accel, tool, wobj and move to start pos
        rob_client.pre_procedure()

        for i, cylinder in enumerate(clay_cylinders):
            current_bullet_desc = "Bullet {:03}/{:03} with id {}.".format(
                i, len(clay_cylinders) - 1, cylinder.bullet_id
            )

            rob_client.send(PrintText(current_bullet_desc))
            log.info(current_bullet_desc)

            rob_client.measure_cylinder(cylinder)

        run_data["fab_data"] = clay_cylinders

        with output_path.open(mode="w") as fp:
            json.dump(run_data, fp, cls=CompasObjEncoder)

        rob_client.post_procedure()

