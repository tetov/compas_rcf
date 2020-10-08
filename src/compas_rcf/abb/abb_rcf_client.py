"""Procedures for pick and place operations on ABB robot arms."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import time

from compas.geometry import Translation
from compas_rrc import AbbClient
from compas_rrc import FeedbackLevel
from compas_rrc import Motion
from compas_rrc import MoveToFrame
from compas_rrc import MoveToJoints
from compas_rrc import Noop
from compas_rrc import PrintText
from compas_rrc import ReadWatch
from compas_rrc import SetAcceleration
from compas_rrc import SetDigital
from compas_rrc import SetMaxSpeed
from compas_rrc import SetTool
from compas_rrc import SetWorkObject
from compas_rrc import StartWatch
from compas_rrc import StopWatch
from compas_rrc import TimeoutException
from compas_rrc import WaitTime
from compas_rrc import Zone

from compas_rcf.docker import restart_container
from compas_rcf.robots import FRAME_LIST_TRAJECTORY_TYPE
from compas_rcf.robots import JOINT_TRAJECTORY_TYPE
from compas_rcf.robots import get_trajectory_type
from compas_rcf.robots import joint_trajectory_to_robot_joints_list

log = logging.getLogger(__name__)


class AbbRcfClient(AbbClient):
    DOCKER_IMAGE = "abb-driver"
    # Define external axis, will not be used but required in move cmds
    EXTERNAL_AXIS_DUMMY: list = []
    # Used to filter rob_joints if they are the same as the previous
    LAST_ROB_JOINTS = None

    def __init__(self, ros, rob_conf):
        super().__init__(ros)

        self.pick_place_tool = rob_conf.tools.get("pick_place")

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
                self.zone.travel["joints"],
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
                self.zone.travel["joints"],
            )
        )

        self.send_and_wait(PrintText("Finished"))

    def pick_bullet(self, pick_elem):
        """Send movement and IO instructions to pick up a clay cylinder.

        Uses `fab_conf` set up with command line arguments and configuration
        file.

        Parameter
        ----------
        pick_elem : :class:`~compas_rcf.fab_data.ClayBullet`
            Representation of fabrication element to pick up.
        """
        # change work object before picking
        self.send(SetTool(self.pick_place_tool.name))
        self.send(SetWorkObject(self.wobjs.pick))

        # start watch
        self.send(StartWatch())

        # TODO: Use separate obj for pick elems?
        vector = pick_elem.get_normal() * self.pick_place_tool.elem_pick_egress_dist
        T = Translation(vector)
        egress_frame = pick_elem.get_uncompressed_top_frame().transformed(T)

        self.send(
            MoveToFrame(egress_frame, self.speed.travel, self.zone.travel["frame"])
        )

        self.send(
            MoveToFrame(
                pick_elem.get_uncompressed_top_frame(),
                self.speed.precise,
                self.zone.pick["frame"],
            )
        )

        self.send(WaitTime(self.pick_place_tool.needles_pause))
        self.extend_needles()
        self.send(WaitTime(self.pick_place_tool.needles_pause))

        self.send(
            MoveToFrame(
                egress_frame,
                self.speed.precise,
                self.zone.pick["frame"],
                motion_type=Motion.LINEAR,
            )
        )

        self.send(StopWatch())

        return self.send(ReadWatch())

    def execute_trajectory(
        self, trajectory, speed, zone, blocking=False, stop_at_last=False
    ):
        """Execute joints or frame trajectories.

        Parameters
        ----------
        trajectory : :class:`compas_rcf.robots.JointTrajectory` or :obj:`list` of :class:`compas.geometry.Frame`
            Trajectory defined by joint positions or frames.
        speed : :obj:`float`
            Speed in mm/s.
        zone : :obj:`dict`
            Dictionary with zones defined either in millimeters or using
            ZoneData names for :class:`~compas_rrc.MoveToFrame` and
            :class:`~compas_rrc.MoveToJoints`. E.g. ``{"frame":
            compas_rrc.Zone.Z10, "joints": compas_rrc.Zone.Z50}``.
        blocking : :obj:`bool`, optional
            If execution should be blocked while waiting for the robot to reach
            last trajectory point. Defaults to ``False``
        stop_at_last : :obj:`bool`, optional
            If last trajectory point should be sent as a non fly-by point, i.e.
            should the last trajectory points zone be set to `compas_rrc.Zone.FINE`.

        Raises
        ------
        ValueError
            If the trajectory argument is not a list of frames or a JointTrajectory.
        """  # noqa: E501
        log.debug(f"Trajectory: {trajectory}")

        trajectory_type = get_trajectory_type(trajectory)

        if trajectory_type == JOINT_TRAJECTORY_TYPE:
            log.debug("Identified type: JointTrajectory")
            rrc_method = MoveToJoints
            # Convert JointTrajectoryPoints to robot_joints_list from rrc
            _trajectory = joint_trajectory_to_robot_joints_list(trajectory)
            _zone = zone["joints"]

        elif trajectory_type == FRAME_LIST_TRAJECTORY_TYPE:
            log.debug("Identified type: Frame list")
            rrc_method = MoveToFrame
            _trajectory = trajectory
            _zone = zone["frame"]

        else:
            raise ValueError(f"No trajectory execution function for {trajectory}.")

        send_method = self.send

        for traj_pt in _trajectory[:-1]:  # skip last
            send_method(rrc_method(traj_pt, self.EXTERNAL_AXIS_DUMMY, speed, _zone))

        if blocking:
            send_method = self.send_and_wait
        if stop_at_last:
            _zone = Zone.FINE

        # send last
        send_method(rrc_method(_trajectory[-1], self.EXTERNAL_AXIS_DUMMY, speed, _zone))

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
        log.debug(f"Location frame: {cylinder.location}")

        # change work object before placing
        self.send(SetWorkObject(self.wobjs.place))
        self.send(SetTool(self.pick_place_tool.name))

        # start watch
        self.send(StartWatch())

        # TODO: Tracked in #56. Create attr with list of trajectories between
        # pick and place
        # egresses to give flexibility to number of traj between pick and
        # place
        self.execute_trajectory(
            cylinder.trajectory_pick_egress_to_segment_egress,
            self.speed.travel,
            self.zone.travel,
        )

        self.execute_trajectory(
            cylinder.trajectory_segment_egress_to_place_egress,
            self.speed.travel,
            self.zone.travel,
        )

        self.execute_trajectory(
            cylinder.trajectory_egress_to_top,
            self.speed.precise,
            self.zone.travel,
            stop_at_last=True,
        )

        self.send(WaitTime(self.pick_place_tool.needles_pause))
        self.retract_needles()
        self.send(WaitTime(self.pick_place_tool.needles_pause))

        self.execute_trajectory(
            cylinder.trajectory_top_to_compressed_top,
            self.speed.precise,
            self.zone.push,
        )
        # TODO: make this frame compatible, maybe set trajectory to either
        # reverse last of egress or frame and execute trajectory?
        last_pt_compressed_top_to_top = joint_trajectory_to_robot_joints_list(
            cylinder.trajectory_compressed_top_to_top
        )[-1]

        self.send(
            MoveToJoints(
                last_pt_compressed_top_to_top,
                self.EXTERNAL_AXIS_DUMMY,
                self.speed.precise,
                self.zone.travel["joints"],
            )
        )

        last_pt_top_to_egress = joint_trajectory_to_robot_joints_list(
            cylinder.trajectory_top_to_egress
        )[-1]

        self.send(
            MoveToJoints(
                last_pt_top_to_egress,
                self.EXTERNAL_AXIS_DUMMY,
                self.speed.travel,
                self.zone.travel["joints"],
            )
        )

        self.execute_trajectory(
            cylinder.trajectory_place_egress_to_segment_egress,
            self.speed.travel,
            self.zone.travel,
        )

        self.execute_trajectory(
            cylinder.trajectory_segment_egress_to_pick_egress,
            self.speed.travel,
            self.zone.travel,
        )

        self.send(StopWatch())

        return self.send(ReadWatch())

    def retract_needles(self):
        """Send signal to retract needles on pick and place tool."""
        pin = self.pick_place_tool.io_pin_needles
        state = self.pick_place_tool.retract_signal

        self.send(SetDigital(pin, state))

        log.debug("IO {} set to {}.".format(pin, state))

    def extend_needles(self):
        """Send signal to extend needles on pick and place tool."""
        pin = self.pick_place_tool.io_pin_needles
        state = self.pick_place_tool.extend_signal

        self.send(SetDigital(pin, state))

        log.debug("IO {} set to {}.".format(pin, state))
