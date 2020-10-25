"""Module for class AbbRcfClient, a client object made for the RCF fab process."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import time

import compas_rrc
from compas.geometry import Translation
from compas_rrc import Motion
from compas_rrc import MoveToJoints
from compas_rrc import MoveToRobtarget

from rapid_clay_formations_fab.abb import DRIVER_CONTAINER_NAME
from rapid_clay_formations_fab.docker import restart_container
from rapid_clay_formations_fab.robots import MinimalTrajectory

log = logging.getLogger(__name__)


class AbbRcfClient(compas_rrc.AbbClient):
    """Robot communication client for RCF fabrication process.

    Subclass of :class:`compas_rrc.AbbClient` with process specific methods.

    Parameters
    ----------
    ros : :class:`compas_fab.backends.ros.RosClient`
        ROS client for communcation with ABB controller.
    rob_conf : :class:`confuse.AttrDict`
        Configuration namespace created from configuration file and command line
        arguments.

    Class attributes
    ----------------
    EXTERNAL_AXES_DUMMY : :class:`compas_rrc.ExternalAxes`
        Dummy object used for :class:`compas_rrc.MoveToRobtarget` and
        :class:`MoveToJoints` objects.
    """

    # Define external axes, will not be used but required in move cmds
    EXTERNAL_AXES_DUMMY = compas_rrc.ExternalAxes()

    def __init__(self, ros, rob_conf):
        super().__init__(ros)

        self.pick_place_tool = rob_conf.tools.get("pick_place")

        self.wobjs = rob_conf.wobjs

        self.global_speed_accel = rob_conf.robot_movement.global_speed_accel

        self.set_joint_pos = rob_conf.robot_movement.set_joint_pos

        self.speed = rob_conf.robot_movement.speed
        self.zone = rob_conf.robot_movement.zone

        self.docker_cfg = rob_conf.docker

    def confirm_start(self):
        """Stop program and prompt user to press play on pendant to resume."""
        self.send(compas_rrc.PrintText("Press play when ready."))
        self.send(compas_rrc.Stop())

    def ping(self, timeout=10):
        """Ping ABB robot controller.

        Parameters
        ----------
        timeout : :obj:`float`, optional
            Timeout for reply. Defaults to ``10``.

        Raises
        ------
        :exc:`TimeoutError`
            If no reply is returned before timeout.
        """
        self.send_and_wait(
            compas_rrc.Noop(feedback_level=compas_rrc.FeedbackLevel.DONE),
            timeout=timeout,
        )

    def check_reconnect(self, timeout_ping=5, wait_after_up=2, tries=3):
        """Check connection to ABB controller and restart abb-driver if necessary.

        Parameters
        ----------
        timeout_ping : :obj:`float`, optional
            Timeout for ping response.
        wait_after_up : :obj:`float`, optional
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
            except compas_rrc.TimeoutException:
                log.info("No response from controller, restarting abb-driver service.")
                restart_container(DRIVER_CONTAINER_NAME)
                time.sleep(self.docker_cfg.sleep_after_up)
        else:
            raise compas_rrc.TimeoutException("Failed to connect to robot.")

    def pre_procedure(self):
        """Pre fabrication setup, speed, acceleration and initial pose."""
        # for safety
        self.retract_needles()

        # Set Acceleration
        self.send(
            compas_rrc.SetAcceleration(
                self.global_speed_accel.accel, self.global_speed_accel.accel_ramp
            )
        )
        log.debug("Acceleration values set.")

        # Set Max Speed
        self.send(
            compas_rrc.SetMaxSpeed(
                self.global_speed_accel.speed_override,
                self.global_speed_accel.speed_max_tcp,
            )
        )
        log.debug("Speed set.")

        # Initial configuration
        log.debug("Sending move to safe joint position")
        self.send_and_wait(
            MoveToJoints(
                self.set_joint_pos.start,
                self.EXTERNAL_AXES_DUMMY,
                self.speed.travel,
                self.zone.travel,
            )
        )

    def post_procedure(self):
        """Post fabrication procedure."""
        self.retract_needles()

        log.debug("Sending move to safe joint position.")
        self.send(
            MoveToJoints(
                self.set_joint_pos.end,
                self.EXTERNAL_AXES_DUMMY,
                self.speed.travel,
                self.zone.travel,
            )
        )

        self.send(compas_rrc.PrintText("Finished"))

    def pick_element(self, element):
        """Send movement and IO instructions to pick up fabrication element.

        Parameter
        ----------
        element : :class:`~rapid_clay_formations_fab.fab_data.FabricationElement`
            Representation of fabrication element to pick up.
        """
        self.send(compas_rrc.SetTool(self.pick_place_tool.name))
        log.debug("Tool {self.pick_place_tool.name} set.")
        self.send(compas_rrc.SetWorkObject(self.wobjs.pick))
        log.debug(f"Work object {self.wobjs.pick} set.")

        # start watch
        self.send(compas_rrc.StartWatch())

        # TODO: Use separate obj for pick elems?
        vector = element.get_normal() * self.pick_place_tool.elem_pick_egress_dist
        T = Translation(vector)
        egress_frame = element.get_uncompressed_top_frame().transformed(T)

        self.send(
            MoveToRobtarget(
                egress_frame,
                self.EXTERNAL_AXES_DUMMY,
                self.speed.travel,
                self.zone.travel,
            )
        )

        self.send(
            MoveToRobtarget(
                element.get_uncompressed_top_frame(),
                self.EXTERNAL_AXES_DUMMY,
                self.speed.pick_place,
                self.zone.pick,
            )
        )

        self.send(compas_rrc.WaitTime(self.pick_place_tool.needles_pause))
        self.extend_needles()
        self.send(compas_rrc.WaitTime(self.pick_place_tool.needles_pause))

        self.send(
            MoveToRobtarget(
                egress_frame,
                self.EXTERNAL_AXES_DUMMY,
                self.speed.pick_place,
                self.zone.pick,
                motion_type=Motion.LINEAR,
            )
        )

        self.send(compas_rrc.StopWatch())

        return self.send(compas_rrc.ReadWatch())

    def execute_trajectory(
        self,
        trajectory,
        speed,
        zone,
        blocking=False,
        stop_at_last=False,
        motion_type=Motion.JOINT,
    ):
        """Execute a :class:`~compas_fab.JointTrajectory`.

        Parameters
        ----------
        trajectory : :class:`rapid_clay_formations_fab.robots.JointTrajectory`
            Trajectory defined by trajectory points, i.e. configurations.
        speed : :obj:`float`
            Speed in mm/s.
        zone : :obj:`dict`
            Zone defined either in millimeters or using
            :class:`compas_rrc.ZoneData` names.
        blocking : :obj:`bool`, optional
            If execution should be blocked while waiting for the robot to reach
            last trajectory point. Defaults to ``False``
        stop_at_last : :obj:`bool`, optional
            If last trajectory point should be sent as a non fly-by point, i.e.
            should the last trajectory points zone be set to `compas_rrc.Zone.FINE`.
        """
        kwargs = {}
        if trajectory.trajectory_type == MinimalTrajectory.JOINT_TRAJECTORY:
            trajectory_pts = trajectory.to_robot_joints()
            instruction = MoveToJoints

        elif trajectory.trajectory_type == MinimalTrajectory.FRAME_TRAJECTORY:
            trajectory_pts = trajectory.points
            instruction = MoveToRobtarget
            kwargs["motion_type"] = motion_type
        else:
            raise RuntimeError("Trajectory not recognized: {}".format(trajectory))

        for pt in trajectory_pts[:-1]:  # skip last
            self.send(instruction(pt, self.EXTERNAL_AXES_DUMMY, speed, zone, **kwargs))

        if blocking:
            send_method_last_pt = self.send_and_wait
        else:
            send_method_last_pt = self.send

        if stop_at_last:
            zone = compas_rrc.Zone.FINE

        # send last
        send_method_last_pt(
            instruction(
                trajectory_pts[-1], self.EXTERNAL_AXES_DUMMY, speed, zone, **kwargs
            )
        )

    def place_element(self, element):
        """Send movement and IO instructions to place a fabrication element.

        Uses `fab_conf` set up with command line arguments and configuration
        file.

        Parameters
        ----------
        element : :class:`rapid_clay_formations_fab.fab_data.FabricationElement`
            Element to place.

        Returns
        -------
        :class:`compas_rrc.FutureResult`
            Object which blocks while waiting for feedback from robot. Calling result on
            this object will return the time the procedure took.
        """
        log.debug(f"Location frame: {element.location}")

        self.send(compas_rrc.SetTool(self.pick_place_tool.name))
        log.debug(f"Tool {self.pick_place_tool.name} set.")
        self.send(compas_rrc.SetWorkObject(self.wobjs.place))
        log.debug(f"Work object {self.wobjs.place} set.")

        # start watch
        self.send(compas_rrc.StartWatch())

        for trajectory in element.travel_trajectories:
            self.execute_trajectory(
                trajectory,
                self.speed.travel,
                self.zone.travel,
            )

        # Execute trajectories in place motion until the last
        for trajectory in element.place_trajectories[:-1]:
            self.execute_trajectory(
                trajectory, self.speed.travel, self.zone.travel, stop_at_last=True
            )

        # Before executing last place trajectory, retract the needles.
        self.retract_needles()
        # Wait to let needles retract fully.
        self.send(compas_rrc.WaitTime(self.pick_place_tool.needles_pause))

        # Last place motion
        self.execute_trajectory(
            element.place_trajectories[-1],
            self.speed.pick_place,
            self.zone.place,
            stop_at_last=True,
            motion_type=Motion.LINEAR,
        )

        self.execute_trajectory(
            element.return_place_trajectories[0],
            self.speed.pick_place,
            self.zone.place,
        )

        for trajectory in element.return_place_trajectories[1:]:
            self.execute_trajectory(trajectory, self.speed.travel, self.zone.travel)

        for trajectory in element.return_travel_trajectories:
            self.execute_trajectory(
                trajectory,
                self.speed.travel,
                self.zone.travel,
            )

        self.send(compas_rrc.StopWatch())

        return self.send(compas_rrc.ReadWatch())

    def retract_needles(self):
        """Send signal to retract needles on pick and place tool."""
        pin = self.pick_place_tool.io_pin_needles
        state = self.pick_place_tool.retract_signal

        self.send(compas_rrc.SetDigital(pin, state))

        log.debug(f"IO {pin} set to {state}.")

    def extend_needles(self):
        """Send signal to extend needles on pick and place tool."""
        pin = self.pick_place_tool.io_pin_needles
        state = self.pick_place_tool.extend_signal

        self.send(compas_rrc.SetDigital(pin, state))

        log.debug(f"IO {pin} set to {state}.")
