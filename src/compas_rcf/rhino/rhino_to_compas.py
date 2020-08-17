"""Most of these are in compas >=0.15 but compas_fab is not there yet."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
import compas.geometry as cg
from compas_rhino.geometry import RhinoMesh

try:
    import Rhino
    import Rhino.Geometry as rg
except ImportError:
    compas.raise_if_ironpython()


def rgpoint_to_cgpoint(pt):
    # type: (Rhino.Geometry.Point3d) -> compas.geometry.Point
    """Convert :class:`Rhino.Geometry.Point3d` to :class:`compas.geometry.Point`.

    Parameters
    ----------
    pt : :class:`Rhino.Geometry.Point3d`
        Plane object to convert

    Returns
    -------
    :class:`compas.geometry.Point`
        Resulting point object
    """
    return cg.Point(pt.X, pt.Y, pt.Z)


def rgvector_to_cgvector(v):
    # type: (Rhino.Geometry.Vector3d) -> compas.geometry.Vector
    """Convert :class:`Rhino.Geometry.Vector3d` to :class:`compas.geometry.Vector`.

    Parameters
    ----------
    v : :class:`Rhino.Geometry.Vector3d`
        Vector object to convert

    Returns
    -------
    :class:`compas.geometry.Vector`
        Resulting vector object
    """
    return cg.Vector(v.X, v.Y, v.Z)


def rgline_to_cgline(line):
    # type: (Rhino.Geometry.Line) -> compas.geometry.Line
    """Convert :class:`Rhino.Geometry.Line` to :class:`compas.geometry.Line`.

    Parameters
    ----------
    line : :class:`Rhino.Geometry.Line`
        Line object to convert

    Returns
    -------
    :class:`compas.geometry.Line`
        Resulting line object
    """
    return cg.Line(rgpoint_to_cgpoint(line.From), rgpoint_to_cgpoint(line.To))


def rgplane_to_cgplane(plane):
    # type: (Rhino.Geometry.Plane) -> compas.geometry.Plane
    """Convert :class:`Rhino.Geometry.Plane` to :class:`compas.geometry.Plane`.

    Parameters
    ----------
    plane : :class:`Rhino.Geometry.Plane`
        Plane object to convert

    Returns
    -------
    :class:`compas.geometry.Plane`
        Resulting plane object

    Notes
    -----
    Unlike a :class:`Rhino.Geometry.Plane` the :class:`compas.geometry.Plane`
    does not store X-axis and Y-axis vectors. See
    :meth:`compas.geometry.Frame.from_plane` docstring.
    """
    return cg.Plane(
        rgpoint_to_cgpoint(plane.Origin), rgvector_to_cgvector(plane.Normal)
    )


def rgplane_to_cgframe(plane):
    # type: (Rhino.Geometry.Plane) -> compas.geometry.Frame
    """Convert :class:`Rhino.Geometry.Plane` to :class:`compas.geometry.Frame`.

    Parameters
    ----------
    plane : :class:`Rhino.Geometry.Plane`
        Plane object to convert

    Returns
    -------
    :class:`compas.geometry.Frame`
        Resulting frame object
    """
    pt = rgpoint_to_cgpoint(plane.Origin)
    xaxis = rgvector_to_cgvector(plane.XAxis)
    yaxis = rgvector_to_cgvector(plane.YAxis)
    return cg.Frame(pt, xaxis, yaxis)


def rgtransform_to_matrix(rgM):
    # type: (Rhino.Geometry.Transform) -> list
    """Convert :class:`Rhino.Geometry.Transform` to transformation matrix.

    Parameters
    ----------
    rgM : :class:`Rhino.Geometry.Transform`

    Returns
    -------
    :class:`list` of :class:`list` of :class:`float`.
    """
    M = [[rgM.Item[i, j] for j in range(4)] for i in range(4)]
    return M


def rgmesh_to_cgmesh(mesh, cls=None):
    return RhinoMesh.from_geometry(mesh).to_compas(cls=cls)


def _test_functions():
    # rgpoint_to_cgpoint
    pt = rgpoint_to_cgpoint(rg.Point3d(3, 2, 1))
    if pt.data != [3.0, 2.0, 1.0]:
        raise Exception("rgpoint_to_cgpoint failed")

    # rgvector_to_cgvector
    v = rgvector_to_cgvector(rg.Vector3d(3, 2, 1))
    if not v.length > 3.7 and not v.length < 3.8:
        raise Exception("rgvector_to_cgvector failed")

    # rgline_cgline
    line = rgline_to_cgline(rg.Line(rg.Point3d(3, 2, 1), rg.Vector3d(1, 1, 0), 5.0))
    if not isinstance(line.midpoint.z, float):
        raise Exception("rgline_to_cgline failed")

    # rgplane_to_cgframe
    frame = rgplane_to_cgframe(rg.Plane(rg.Point3d(1, 3, 2), rg.Vector3d(2, -1, 1)))
    if (
        frame.quaternion.__repr__
        != "Quaternion(0.713799, 0.462707, 0.285969, 0.441152)"
    ):
        raise Exception("rgplane_to_cgframe failed")

    # rgtransform_to_matrix
    matrix = rg.Transform.ZeroTransformation

    zero_matrix = [
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
    if rgtransform_to_matrix(matrix) != zero_matrix:
        raise Exception("rgtransform_to_matrix failed.")


if __name__ == "__main__":
    _test_functions()
