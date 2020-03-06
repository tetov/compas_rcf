"""Most of these are in compas >=0.15 but compas_fab is not there yet."""
# flake8: noqa: F821
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas import IPY
import compas.geometry as cg

if IPY:
    import Rhino.Geometry as rg


def cgpoint_to_rgpoint(pt):  # type: (compas.geometry.Point) -> Rhino.Geometry.Point3d
    """Convert :class:`compas.geometry.Point` to :class:`Rhino.Geometry.Point3d`.

    Parameters
    ----------
    :class:`compas.geometry.Point`
        Point object to convert.

    Returns
    -------
    :class:`Rhino.Geometry.Point3d`
        Resulting Point3d object.
    """
    return rg.Point3d(*pt.data)


def cgvector_to_rgvector(
    v,
):  # type: (compas.geometry.Vector) -> Rhino.Geometry.Vector3d
    """Convert :class:`compas.geometry.Vector` to :class:`Rhino.Geometry.Vector3d`.

    Parameters
    ----------
    :class:`compas.geometry.Vector`
        Vector object to convert.

    Returns
    -------
    :class:`Rhino.Geometry.Vector3d`
        Resulting Vector3d object.
    """
    # TODO: Implement in compas
    return rg.Vector3d(*v.data)


def cgline_to_rgline(line):  # type: (compas.geometry.Line) -> Rhino.Geometry.Line
    """Convert :class:`compas.geometry.Line` to :class:`Rhino.Geometry.Line`.

    Parameters
    ----------
    :class:`compas.geometry.Line`
        Point object to convert.

    Returns
    -------
    :class:`Rhino.Geometry.Line`
        Resulting Line object.
    """
    return rg.Line(cgpoint_to_rgpoint(line.start), cgpoint_to_rgpoint(line.end))


def cgplane_to_rgplane(
    cgplane,
):  # type: (compas.geometry.Plane) -> Rhino.Geometry.Plane
    """Convert :class:`compas.geometry.Plane` to :class:`Rhino.Geometry.Plane`.

    Parameters
    ----------
    :class:`compas.geometry.Plane`
        Plane to convert.

    Returns
    -------
    :class:`Rhino.Geometry.Plane`
        Resulting plane.
    """
    return rg.Plane(
        cgpoint_to_rgpoint(cgplane.point), cgvector_to_rgvector(cgplane.normal)
    )


def cgframe_to_rgplane(frame):  # type: (compas.geometry.Frame) -> Rhino.Geometry.Plane
    """Convert :class:`compas.geometry.Frame` to :class:`Rhino.Geometry.Plane`.

    Parameters
    ----------
    :class:`compas.geometry.Frame`
        Frame to convert.

    Returns
    -------
    :class:`Rhino.Geometry.Plane`
        Resulting plane.
    """
    plane = cg.Plane(frame.point, frame.normal)
    return cgplane_to_rgplane(plane)


def matrix_to_rgtransform(M):
    """Create :class:`Rhino.Geometry.Transform` from a transformation matrix.

    Parameters
    ----------
    M : list of lists of floats
        Transformation matrix.

    Returns
    -------
    :class:`Rhino.Geometry.Transform`
    """
    rgM = rg.Transform()
    for i, row in enumerate(M):
        for j, val in enumerate(row):
            rgM[i, j] = val
    return rgM


if __name__ == "__main__":

    # test cgpoint_to_rgpoint
    point = cgpoint_to_rgpoint(cg.Point(1, 2, 3))
    assert point.Z == 3.0

    # test cgvector_to_rgvector
    vector = cgvector_to_rgvector(cg.Vector(5, 1, 9))
    assert vector.Unitize()

    # test cgline_to_rgline
    line = cgline_to_rgline(cg.Line([1, 2, 3], [3, 2, 1]))
    assert line.Direction == rg.Vector3d(2, 0, -2)

    # test frame_to_plane
    plane = cgframe_to_rgplane(cg.Frame([1, 3, -1], [1, 1, 2], [0, 1, 1]))
    assert isinstance(plane.Normal, rg.Vector3d)

    # matrix_to_rgtransform
    R = cg.Rotation.from_basis_vectors([1, 2, 0], [2, 1, 3])
    assert isinstance(matrix_to_rgtransform(R), rg.Transform)
