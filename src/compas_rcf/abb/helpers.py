"""Helpers for scripts interacting with ABB robots or RAPID code."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import math
import time
from os.path import join

from compas import IPY
from compas.geometry import Frame
from compas_rrc import FeedbackLevel
from compas_rrc import Noop

from compas_rcf import HERE
from compas_rcf.docker import compose_up
from compas_rcf.utils import ensure_frame

if IPY:
    from compas_rcf.rhino import cgframe_to_rgplane

__all__ = [
    "ZONE_DICT",
    "DOCKER_COMPOSE_PATHS",
    "ROBOT_IPS",
    "ping",
    "check_reconnect",
    "RapidToolData",
]

log = logging.getLogger(__name__)

# Describes the valid zone data definitions.
ZONE_DICT = {
    "FINE": -1,
    "Z0": 0,
    "Z1": 1,
    "Z5": 5,
    "Z10": 10,
    "Z15": 15,
    "Z20": 20,
    "Z30": 30,
    "Z40": 40,
    "Z50": 50,
    "Z60": 60,
    "Z80": 80,
    "Z100": 100,
    "Z150": 150,
    "Z200": 200,
}

_path_from_pkg = ["docker", "compose_files", "abb"]
_compose_folder = join(HERE, *_path_from_pkg)
_base_name = "driver-base-docker-compose.yml"
_driver_name = "driver-docker-compose.yml"

DOCKER_COMPOSE_PATHS = {
    "base": join(_compose_folder, _base_name),
    "driver": join(_compose_folder, _driver_name),
}

ROBOT_IPS = {"real": "192.168.125.1", "virtual": "host.docker.internal"}


def ping(client, timeout=10):
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
    feedback = client.send(Noop(feedback_level=FeedbackLevel.DONE))

    try:
        return feedback.result(timeout=timeout)
    except Exception as e:
        if e.args[0] == "Timeout: future result not available":
            raise TimeoutError(e.args)
        else:
            raise


def check_reconnect(client, target="virtual", timeout_ping=5, wait_after_up=2):
    """Check connection to ABB controller and restart abb-driver if necessary.

    Parameters
    ----------
    client : :class:`compas_rrc.AbbClient`
        Client connected to controller.
    target : :class:`str`, optional
        One of ``"virtual"`` or ``"real"``. Defaults to ``"virtual"``.
    timeout_ping : :class:`float`, optional
        Timeout for ping response.
    wait_after_up : :class:`float`, optional
        Time to wait to ping after `abb-driver` container started.

    Raises
    ------
    :exc:`TimeoutError`
        If no reply is returned before timeout.
    """
    env_vars = {"ROBOT_IP": ROBOT_IPS[target]}

    for i in range(3):
        try:
            log.debug("Pinging robot")
            ping(client, timeout_ping)
            log.debug("Breaking loop after successful ping.")
            break
        except TimeoutError:
            log.info("No response from controller, restarting abb-driver service.")
            compose_up(
                DOCKER_COMPOSE_PATHS["driver"], force_recreate=True, env_vars=env_vars,
            )
            log.debug(
                "Compose up for abb_driver with robot-ip={}".format(
                    env_vars["ROBOT_IP"]
                )
            )
            time.sleep(wait_after_up)
    else:
        raise TimeoutError("Failed to connect to robot")


class RapidToolData(object):
    """Create Rapid ToolData.

    Parameters
    ----------
    tcp_coord : :class:`list` of class:`float`
        Coordinate of tool center point.
    tcp_quaternion : :class:`list` of :class:`float`
        Rotation of tool center plane in quaternions.
    cog_coord : :class:`list` of :class:`float`, optional
        Coordinates of center of gravity of tool. Defaults to ``[0, 0, 100]``.
    name : :class:`str`, optional
        Name of tool, used as variable name in :meth:`get_rapid_tooldata`.
        Defaults to ``"tool"``.
    weight : :class:`float`, optional
        Tool weight in kg. Defaults to ``5.0``.
    tolerance : :class:`int`, optional
        Tolerance used in Rapid tooldata string given by
        :meth:`get_rapid_tooldata`. Defaults to ``1e-6``.

    Note
    ----
    Axes of moment and inertia not implemented
    """

    RAPID_TOOLDATA_FORMAT = (
        "TASK PERS tooldata {}"
        + ":=[TRUE,[[{},{},{}],[{},{},{},{}]],"
        + "[{},[{},{},{}],[1,0,0,0],0,0,0]];"
    )

    def __init__(
        self,
        tcp_coord,
        tcp_quaternion,
        cog_coord=[0, 0, 100],
        name="tool",
        weight=5.0,
        tolerance=1e-6,
    ):
        self.tcp_coord = tcp_coord
        self.tcp_quaternion = tcp_quaternion
        self.cog_coord = cog_coord
        self.name = name
        self.weight = weight
        self.tolerance = tolerance

    @property
    def tcp_frame(self):
        """TCP represented as a :class:`compas.geometry.Frame`."""
        return Frame.from_quaternion(self.tcp_quaternion, point=self.tcp_coord)

    @property
    def tcp_plane(self):
        """TCP represented as a :class:`Rhino.Geometry.Plane`."""
        return cgframe_to_rgplane(self.tcp_frame)

    @classmethod
    def from_frame_point(cls, tcp_frame, cog_pt=None, **kwargs):
        """Create RapidToolData object from :class:`compas.Geometry.Primitive` objects.

        Parameters
        ----------
        tcp_frame : :class:`compas.geometry.Frame`
            Frame at tool center plane.
        cog_pt : :class:`compas.geometry.Point`, optional
            Point at tool center of gravity.
        name : :class:`str`, optional
        weight : :class:`float`, optional
            Tool weight in kg

        Returns
        -------
        :class:`RapidToolData`
        """
        tcp_coord = tcp_frame.point.data
        tcp_quaternion = tcp_frame.quaternion.wxyz

        if cog_pt:
            kwargs.update({"cog_coord": cog_pt.data})

        return cls(tcp_coord, tcp_quaternion, **kwargs)

    @classmethod
    def from_plane_point(cls, tcp_plane, cog_pt=None, **kwargs):
        """Create RapidToolData object from :class:`Rhino.Geometry.GeometryBase` objects.

        Parameters
        ----------
        tcp_plane : :class:`Rhino.Geometry.Plane`
            Plane at tool center plane.
        cog_pt : :class:`Rhino.Geometry.Point3d`, optional
            Point at tool center of gravity.
        name : str, optional
        weight : float, optional
            Tool weight in kg

        Returns
        -------
        :class:`RapidToolData`
        """
        tcp_coord = [tcp_plane.Origin.X, tcp_plane.Origin.Y, tcp_plane.Origin.Z]

        tcp_frame = ensure_frame(tcp_plane)
        tcp_quaternion = tcp_frame.quaternion.wxyz

        if cog_pt:
            cog_coord = [cog_pt.X, cog_pt.Y, cog_pt.Z]
            kwargs.update({"cog_coord": cog_coord})

        return cls(tcp_coord, tcp_quaternion, **kwargs)

    def get_rapid_tooldata(self):
        """Generate Rapid tooldata.

        Returns
        -------
        :class:`str`
        """
        data = self.tcp_coord + self.tcp_quaternion + [self.weight] + self.cog_coord
        formatted_data = [self._float_str(x) for x in data]

        return self.RAPID_TOOLDATA_FORMAT.format(self.name, *formatted_data)

    def _float_str(self, n):
        """Format float as string with given tolerance.

        Arguments
        ---------
        n : :class:`float` or :class:`int`
            Number to format

        Returns
        -------
        :class:`str`
        """
        # Get tolerance as number of decimals
        tol = -1 * math.floor(math.log(self.tolerance, 10))

        return "{:.{tol}f}".format(float(n), tol=int(tol))
