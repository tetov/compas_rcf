"""Procedures for pick and place operations on ABB robot arms."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import math
import time

from compas.geometry import Translation
from compas_fab.robots import JointTrajectory
from compas_rrc import AbbClient
from compas_rrc import FeedbackLevel
from compas_rrc import MoveToFrame
from compas_rrc import MoveToJoints
from compas_rrc import Noop
from compas_rrc import PrintText
from compas_rrc import ReadWatch
from compas_rrc import RobotJoints
from compas_rrc import SetAcceleration
from compas_rrc import SetDigital
from compas_rrc import SetMaxSpeed
from compas_rrc import SetTool
from compas_rrc import SetWorkObject
from compas_rrc import StartWatch
from compas_rrc import StopWatch
from compas_rrc import TimeoutException
from compas_rrc import WaitTime

from compas_rcf.docker import restart_container
from compas_rcf.sensing import get_distance_measurement

log = logging.getLogger(__name__)


class AbbRcfClient(AbbClient):
    DOCKER_IMAGE = "abb-driver"
    # Define external axis, will not be used but required in move cmds
    EXTERNAL_AXIS_DUMMY: list = []

    def __init__(self, ros, rob_conf):
        super().__init__(ros)

        self.pick_place_tool = rob_conf.tools.get("pick_place")
        self.dist_sensor_tool = rob_conf.tools.get("dist_sensor")

        self.wobjs = rob_conf.wobjs

        self.global_speed_accel = rob_conf.robot_movement.global_speed_accel

        self.set_joint_pos = rob_conf.robot_movement.set_joint_pos

        self.speed = rob_conf.robot_movement.speed
        self.zone = rob_conf.robot_movement.zone

        self.docker_cfg = rob_conf.docker

    def ping(self, timeout=10):
        """Ping ABB robot controller.

        Parameters
        ----------
        client : :class:`compas_rrc.AbbClient`
            Client connected to controller.
        timeout : :class:`float`, optional
            Timeout for reply. Defaults to ``10``.

        Raises
        ------
        :exc:`TimeoutError`
            If no reply is returned before timeout.
        """
        self.send_and_wait(Noop(feedback_level=FeedbackLevel.DONE), timeout=timeout)

    def check_reconnect(self, timeout_ping=5, wait_after_up=2, tries=3):
        """Check connection to ABB controller and restart abb-driver if necessary.

        Parameters
        ----------
        client : :class:`compas_rrc.AbbClient`
            Client connected to controller.
        timeout_ping : :class:`float`, optional
            Timeout for ping response.
        wait_after_up : :class:`float`, optional
            Time to wait to ping after `abb-driver` container started.

        Raises
        ------
        :exc:`TimeoutError`
            If no reply is returned before timeout.
        """
        for _ in range(tries):
            try:
                log.debug("Pinging robot")
                self.ping(self.docker_cfg.timeout_ping)
                log.debug("Breaking loop after successful ping.")
                break
            except TimeoutException:
                log.info("No response from controller, restarting abb-driver service.")
                restart_container(self.DOCKER_IMAGE)
                time.sleep(self.docker_cfg.sleep_after_up)
        else:
            raise TimeoutException("Failed to connect to robot.")

    def pre_procedure(self):
        """Pre fabrication setup, speed, acceleration, tool, work object and initial pose.

        Uses ``fab_conf`` set up using
        :func:`compas_rcf.fab_data.interactive_conf_setup` for fabrication settings.

        Parameters
        ----------
        client : :class:`compas_rrc.AbbClient`
            Client connected to controller procedure should be sent to.
        """
        # for safety
        self.retract_needles()

        self.send(SetTool(self.pick_place_tool.name))
        log.debug("Tool {} set.".format(self.pick_place_tool.name))
        self.send(SetWorkObject(self.wobjs.place))
        log.debug("Work object {} set.".format(self.wobjs.place))

        # Set Acceleration
        self.send(
            SetAcceleration(
                self.global_speed_accel.accel, self.global_speed_accel.accel_ramp
            )
        )
        log.debug("Acceleration values set.")

        # Set Max Speed
        self.send(
            SetMaxSpeed(
                self.global_speed_accel.speed_override,
                self.global_speed_accel.speed_max_tcp,
            )
        )
        log.debug("Speed set.")

        # Initial configuration
        self.send(
            MoveToJoints(
                self.set_joint_pos.start,
                self.EXTERNAL_AXIS_DUMMY,
                self.speed.travel,
                self.zone.travel,
            )
        )
        log.debug("Sent move to safe joint position")

    def post_procedure(self):
        """Post fabrication procedure, end pose and closing and termination of client.

        Uses ``fab_conf`` set up using
        :func:`compas_rcf.fab_data.interactive_conf_setup` for fabrication settings.

        Parameters
        ----------
        client : :class:`compas_rrc.AbbClient`
        """
        self.retract_needles()

        self.send(
            MoveToJoints(
                self.set_joint_pos.end,
                self.EXTERNAL_AXIS_DUMMY,
                self.speed.travel,
                self.zone.travel,
            )
        )

        self.send_and_wait(PrintText("Finished"))

    def pick_bullet(self, cylinder):
        """Send movement and IO instructions to pick up a clay cylinder.

        Uses `fab_conf` set up with command line arguments and configuration
        file.

        Parameters
        ----------
        client : :class:`compas_rrc.AbbClient`
        picking_frame : :class:`compas.geometry.Frame`
            Target frame to pick up cylinder
        """
        # change work object before picking
        self.send(SetTool(self.pick_place_tool.name))
        self.send(SetWorkObject(self.wobjs.pick))

        # start watch
        self.send(StartWatch())

        self.send(
            MoveToFrame(
                cylinder.get_egress_frame(), self.speed.travel, self.zone.travel
            )
        )

        self.send(
            MoveToFrame(
                cylinder.get_uncompressed_top_frame(),
                self.speed.travel,
                self.zone.precise,
            )
        )

        self.send(WaitTime(self.pick_place_tool.needles_pause))
        self.extend_needles()
        self.send(WaitTime(self.pick_place_tool.needles_pause))

        self.send(
            MoveToFrame(
                cylinder.get_egress_frame(), self.speed.precise, self.zone.precise
            )
        )

        self.send(StopWatch())

        return self.send(ReadWatch())

    def execute_trajectory(self, trajectory):
        trajectory_type = self._get_trajectory_type(trajectory)
        if trajectory_type == "JointTrajectory":
            execute_func = self._execute_joint_trajectory
        elif trajectory_type == "FrameList":
            execute_func = self._execute_frame_trajectory
        else:
            raise ValueError(f"No trajectory execution function for {trajectory}.")

        execute_func(trajectory)

    def _execute_joint_trajectory(self, trajectory):
        robot_joints_list = self.joint_trajectory_to_robot_joints_list(trajectory)

        for rob_joints in robot_joints_list:
            self.send(
                MoveToJoints(
                    rob_joints,
                    self.EXTERNAL_AXIS_DUMMY,
                    self.speed.travel,
                    self.zone.travel,
                )
            )

    def _execute_frame_trajectory(self, trajectory):

        for frame in trajectory:
            self.send(MoveToFrame(frame, self.speed.travel, self.zone.travel))

    def place_bullet(self, cylinder):
        """Send movement and IO instructions to place a clay cylinder.

        Uses `fab_conf` set up with command line arguments and configuration
        file.

        Parameters
        ----------
        client : :class:`compas_rrc.AbbClient`
            Client connected to controller procedure should be sent to.
        cylinder : :class:`compas_rcf.fab_data.ClayBullet`
            cylinder to place.

        Returns
        -------
        :class:`compas_rrc.FutureResult`
            Object which blocks while waiting for feedback from robot. Calling result on
            this object will return the time the procedure took.
        """
        log.debug("Location frame: {}".format(cylinder.location))

        # change work object before placing
        self.send(SetWorkObject(self.wobjs.place))

        # move there with distance sensor TCP active
        self.send(SetTool(self.dist_sensor_tool.name))

        # start watch
        self.send(StartWatch())

        self.execute_trajectory(cylinder.trajectory_to)

        self.send(
            MoveToFrame(
                cylinder.get_egress_frame(), self.speed.travel, self.zone.travel
            )
        )

        if self.dist_sensor_tool.get("port") is not None:
            dist_diff = self.measure_z_diff(cylinder)

            if self.max_z_diff and self.is_dist_diff_ok(dist_diff):
                self.correct_location(cylinder, dist_diff)
            else:
                raise Exception("Unacceptable distance difference.")

        self.send(SetTool(self.pick_place_tool))

        self.send(
            MoveToFrame(
                cylinder.get_uncompressed_top_frame(),
                self.speed.precise,
                self.zone.precise,
            )
        )

        self.send(WaitTime(self.pick_place_tool.needles_pause))
        self.retract_needles()
        self.send(WaitTime(self.pick_place_tool.needles_pause))

        self.send(
            MoveToFrame(
                cylinder.get_compressed_top_frame(),
                self.speed.precise,
                self.zone.precise,
            )
        )

        self.send(
            MoveToFrame(
                cylinder.get_egress_frame(), self.speed.travel, self.zone.travel
            )
        )

        # offset placement frame then safety frame
        self.execute_trajectory(cylinder.trajectory_from)

        self.send(StopWatch())

        return self.send(ReadWatch())

    def retract_needles(self):
        pin = self.pick_place_tool.io_pin_needles
        state = self.pick_place_tool.retract_signal

        self.send(SetDigital(pin, state))

        log.debug("IO {} set to {}.".format(pin, state))

    def extend_needles(self):
        pin = self.pick_place_tool.io_pin_needles
        state = self.pick_place_tool.extend_signal

        self.send(SetDigital(pin, state))

        log.debug("IO {} set to {}.".format(pin, state))

    def measure_z_diff(self, cylinder):

        self.send(WaitTime(1))

        dist_read = get_distance_measurement()
        log.debug("Dist read: {}".format(dist_read))

        self.send(WaitTime(1))

        expected_dist = cylinder.get_egress_frame().point.distance_to_point(
            cylinder.location.point
        )

        dist_diff = expected_dist - dist_read
        log.debug("Dist diff: {}".format(dist_diff))

        return dist_diff

    def is_dist_diff_ok(self, dist_diff):
        return abs(dist_diff) < self.max_z_diff

    @staticmethod
    def correct_location_in_z(cylinder, dist_diff):
        corr_vector = cylinder.get_normal() * dist_diff
        T = Translation(corr_vector)

        cylinder.location.transform(T)

        cylinder.attrs["location_correction"] = corr_vector

    @classmethod
    def from_confuse_conf(cls, ros, conf):
        pass

    @staticmethod
    def _get_trajectory_type(trajectory):
        if isinstance(trajectory, JointTrajectory):
            return "JointTrajectory"
        # Assume its list of frame if not JointTrajectory
        return "FrameList"

    @staticmethod
    def joint_trajectory_to_robot_joints_list(joint_trajectory):
        robot_joints_list = []
        for pt in joint_trajectory.points:
            in_degrees = [math.degrees(pos) for pos in pt.values]
            robot_joints_list.append(RobotJoints(*in_degrees))

        return robot_joints_list
