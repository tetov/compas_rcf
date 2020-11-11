"""Module for class AbbRcfClient, a client object made for the RCF fab process."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import time
import typing

import compas_rrc
import confuse
from compas_fab.backends.ros import RosClient
from compas_fab.robots import Configuration
from compas_fab.robots import to_radians
from compas_rrc import Motion
from compas_rrc import MoveToJoints
from compas_rrc import MoveToRobtarget

from rapid_clay_formations_fab.docker import restart_container
from rapid_clay_formations_fab.fab_data import PlaceElement
from rapid_clay_formations_fab.robots import DRIVER_CONTAINER_NAME
from rapid_clay_formations_fab.robots import MinimalTrajectories
from rapid_clay_formations_fab.robots import MinimalTrajectory
from rapid_clay_formations_fab.robots import PickStation

log = logging.getLogger(__name__)

T = typing.TypeVar("T", bound="AbbRcfClient")


class AbbRcfClient(compas_rrc.AbbClient):
    """Robot communication client for RCF.

    Subclass of :class:`compas_rrc.AbbClient` with some utility methods added.

    Parameters
    ----------
    ros_port : :obj:`int`, optional
        ROS client port for communcation with ABB controller, defaults to 9090.

    Class attributes
    ----------------
    EXTERNAL_AXES_DUMMY : :class:`compas_rrc.ExternalAxes`
        Dummy object used for :class:`compas_rrc.MoveToRobtarget` and
        :class:`MoveToJoints` objects.
    """

    # Define external axes, will not be used but required in move cmds
    EXTERNAL_AXES_DUMMY = compas_rrc.ExternalAxes()

    def __init__(self, ros_port: int = 9090) -> None:
        super().__init__(RosClient(port=ros_port))

    def __enter__(self: T) -> T:
        self.ros.__enter__()
        return self

    def __exit__(self, *args):
        self.close()
        self.terminate()

    def confirm_start(self) -> None:
        """Stop program and prompt user to press play on pendant to resume."""
        self.send(compas_rrc.PrintText("Press play when ready."))
        self.send(compas_rrc.Stop())
        log.info("Press start on pendant when ready")

        # After user presses play on pendant execution resumes:
        self.send(compas_rrc.PrintText("Resuming execution."))

    def ping(self, timeout: float = 10) -> None:
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

    def check_reconnect(
        self,
        timeout_ping: float = 5,
        wait_after_up: float = 2,
        tries: int = 3,
    ):
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
                self.ping(timeout_ping)
                log.debug("Breaking loop after successful ping.")
                break
            except compas_rrc.TimeoutException:
                log.info("No response from controller, restarting abb-driver service.")
                restart_container(DRIVER_CONTAINER_NAME)

                time.sleep(wait_after_up)
        else:
            raise compas_rrc.TimeoutException("Failed to connect to robot.")


class AbbRcfFabricationClient(AbbRcfClient):
    """Robot communication client for RCF fabrication process.

    Subclass of :class:`AbbRcfClient` with fabrication specific methods.

    Parameters
    ----------
    ros : :class:`compas_fab.backends.ros.RosClient`
        ROS client for communcation with ABB controller.
    rob_conf : :class:`confuse.AttrDict`
        Configuration namespace created from configuration file and command line
        arguments.
    pick_station : :class:`rapid_clay_formations_fab.fab_data.PickStation`
        Pick station for fabrication elements.
    """

    def __init__(
        self,
        rob_conf: confuse.AttrDict,
        pick_station: PickStation,
        ros_port: int = 9090,
    ):
        super().__init__(ros_port=ros_port)

        self.pick_place_tool = rob_conf.tools.get("pick_place")

        self.wobjs = rob_conf.wobjs

        self.global_speed_accel = rob_conf.robot_movement.global_speed_accel

        self.joint_positions = rob_conf.robot_movement.joint_positions

        self.speed = rob_conf.robot_movement.speed
        self.zone = rob_conf.robot_movement.zone

        self.docker_cfg = rob_conf.docker

        # Setup pick station
        self.pick_station = pick_station

        if hasattr(self.joint_positions, "travel_trajectory"):
            joint_positions = [
                to_radians(jp) for jp in self.joint_positions.travel_trajectory
            ]
            configurations = [
                Configuration.from_revolute_values(jps) for jps in joint_positions
            ]
            trajectory = MinimalTrajectory(configurations)
            trajectories = MinimalTrajectories([trajectory])

            self.default_travel_trajectories = trajectories
            self.default_return_travel_trajectories = (
                trajectories.reversed_recursively()
            )
            log.debug(
                f"default_travel_trajectories: {self.default_travel_trajectories}"
            )

    def check_reconnect(
        self, timeout_ping: float = None, wait_after_up: float = None, tries: int = 3
    ) -> None:
        """Check connection to ABB controller and restart abb-driver if necessary.

        Parameters
        ----------
        tries : :obj:`int`, optional
            Connection tries, defaults to 3.

        Raises
        ------
        :exc:`TimeoutError`
            If no reply is returned before timeout.
        """
        if not timeout_ping:
            timeout_ping = self.docker_cfg.timeout_ping
        if not wait_after_up:
            wait_after_up = self.docker_cfg.sleep_after_up

        # Fixing mypy warning about incompatible types in super meth call
        assert timeout_ping is not None
        assert wait_after_up is not None

        super().check_reconnect(
            timeout_ping=timeout_ping,
            wait_after_up=wait_after_up,
            tries=tries,
        )

    def pre_procedure(self) -> None:
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
                self.joint_positions.start,
                self.EXTERNAL_AXES_DUMMY,
                self.speed.travel,
                self.zone.travel,
            )
        )

    def post_procedure(self) -> None:
        """Post fabrication procedure."""
        self.retract_needles()

        log.debug("Sending move to safe joint position.")
        self.send(
            MoveToJoints(
                self.joint_positions.end,
                self.EXTERNAL_AXES_DUMMY,
                self.speed.travel,
                self.zone.travel,
            )
        )

        self.send(compas_rrc.PrintText("Finished"))

    def pick_element(self) -> None:
        """Send movement and IO instructions to pick up fabrication element."""
        self.send(compas_rrc.SetTool(self.pick_place_tool.name))
        log.debug(f"Tool {self.pick_place_tool.name} set.")
        self.send(compas_rrc.SetWorkObject(self.wobjs.pick))
        log.debug(f"Work object {self.wobjs.pick} set.")

        element = self.pick_station.get_next_pick_elem()

        self.send(
            MoveToRobtarget(
                element.get_egress_frame(),
                self.EXTERNAL_AXES_DUMMY,
                self.speed.travel,
                self.zone.pick,
            )
        )

        self.send(
            MoveToRobtarget(
                element.get_top_frame(),
                self.EXTERNAL_AXES_DUMMY,
                # TODO: Set up conf for speed pick specificly
                self.speed.travel,
                compas_rrc.Zone.FINE,
            )
        )

        self.extend_needles()
        self.send(compas_rrc.WaitTime(self.pick_place_tool.needles_pause))

        self.send(
            MoveToRobtarget(
                element.get_egress_frame(),
                self.EXTERNAL_AXES_DUMMY,
                self.speed.travel,
                self.zone.pick,
                motion_type=Motion.LINEAR,
            )
        )

    def place_element(self, element: PlaceElement) -> None:
        """Send movement and IO instructions to place a fabrication element.

        Uses `fab_conf` set up with command line arguments and configuration
        file.

        Parameters
        ----------
        element : :class:`rapid_clay_formations_fab.fab_data.PlaceElement`
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

        for trajectory in self._get_travel_trajectories(element):
            self.execute_trajectory(
                trajectory,
                self.speed.travel,
                self.zone.travel,
            )

        place_trajectories = self._get_place_trajectories(element)
        # Execute trajectories in place motion until the last
        for trajectory in place_trajectories[:-1]:
            self.execute_trajectory(
                trajectory, self.speed.travel, self.zone.travel, stop_at_last=True
            )

        # Before executing last place trajectory, retract the needles.
        self.retract_needles()
        # Wait to let needles retract fully.
        self.send(compas_rrc.WaitTime(self.pick_place_tool.needles_pause))

        # Last place motion
        self.execute_trajectory(
            place_trajectories[-1],
            self.speed.pick_place,
            self.zone.place,
            motion_type=Motion.LINEAR,
        )

        return_place_trajectories = self._get_return_place_trajectories(element)
        self.execute_trajectory(
            return_place_trajectories[0],
            self.speed.pick_place,
            self.zone.place,
        )

        for trajectory in return_place_trajectories[1:]:
            self.execute_trajectory(trajectory, self.speed.travel, self.zone.travel)

        return_travel_trajectories = self._get_return_travel_trajectories(element)
        for trajectory in return_travel_trajectories:
            self.execute_trajectory(
                trajectory,
                self.speed.travel,
                self.zone.travel,
            )

    def _get_travel_trajectories(self, element: PlaceElement) -> MinimalTrajectories:
        if element.travel_trajectories:
            return element.travel_trajectories

        return self.default_travel_trajectories

    def _get_return_travel_trajectories(
        self, element: PlaceElement
    ) -> MinimalTrajectories:
        if element.return_travel_trajectories:
            return element.return_travel_trajectories
        if element.travel_trajectories:
            return element.travel_trajectories.reversed_recursively()

        return self.default_return_travel_trajectories

    @staticmethod
    def _get_place_trajectories(element: PlaceElement) -> MinimalTrajectories:
        if element.place_trajectories:
            return element.place_trajectories

        approach = MinimalTrajectory(
            [element.get_egress_frame(), element.get_uncompressed_top_frame()]
        )
        pressing = MinimalTrajectory([element.get_compressed_top_frame()])
        return MinimalTrajectories([approach, pressing])

    def _get_return_place_trajectories(
        self, element: PlaceElement
    ) -> MinimalTrajectories:
        if element.return_place_trajectories:
            return element.return_place_trajectories

        return self._get_place_trajectories(element).reversed_recursively()

    def execute_trajectory(
        self,
        trajectory: MinimalTrajectory,
        speed: float,
        zone: typing.Union[compas_rrc.Zone, int],
        blocking: bool = False,
        stop_at_last: bool = False,
        motion_type: int = Motion.JOINT,
    ) -> None:
        """Execute a :class:`~compas_fab.JointTrajectory`.

        Parameters
        ----------
        trajectory
            Trajectory defined by frames or configurations.
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
        log.debug(f"Trajectory: {trajectory}.")
        kwargs = {}

        if trajectory.trajectory_type == MinimalTrajectory.JOINT_TRAJECTORY:
            trajectory_pts = trajectory.as_robot_joints_points()
            instruction = MoveToJoints

        elif trajectory.trajectory_type == MinimalTrajectory.FRAME_TRAJECTORY:
            trajectory_pts = trajectory.points
            instruction = MoveToRobtarget
            kwargs["motion_type"] = motion_type
        else:
            raise RuntimeError(f"Trajectory not recognized: {trajectory}.")

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

    def retract_needles(self) -> None:
        """Send signal to retract needles on pick and place tool."""
        pin = self.pick_place_tool.io_pin_needles
        state = self.pick_place_tool.retract_signal

        self.send(compas_rrc.SetDigital(pin, state))

        log.debug(f"IO {pin} set to {state}.")

    def extend_needles(self) -> None:
        """Send signal to extend needles on pick and place tool."""
        pin = self.pick_place_tool.io_pin_needles
        state = self.pick_place_tool.extend_signal

        self.send(compas_rrc.SetDigital(pin, state))

        log.debug(f"IO {pin} set to {state}.")
