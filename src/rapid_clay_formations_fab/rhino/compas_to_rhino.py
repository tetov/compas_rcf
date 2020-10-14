"""Most of these are in compas >=0.15 but compas_fab is not there yet."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
import compas.geometry as cg
from compas_ghpython.artists import MeshArtist

try:
    import Rhino
    import Rhino.Geometry as rg
except ImportError:
    compas.raise_if_ironpython()


def cgpoint_to_rgpoint(pt):  # type: (compas.geometry.Point) -> Rhino.Geometry.Point3d
    """Convert :class:`compas.geometry.Point` to :class:`Rhino.Geometry.Point3d`.

    Parameters
    ----------
    pt : :class:`compas.geometry.Point`
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
    v : :class:`compas.geometry.Vector`
        Vector object to convert.

    Returns
    -------
    :class:`Rhino.Geometry.Vector3d`
        Resulting Vector3d object.
    """
    return rg.Vector3d(*v.data)


def cgline_to_rgline(line):  # type: (compas.geometry.Line) -> Rhino.Geometry.Line
    """Convert :class:`compas.geometry.Line` to :class:`Rhino.Geometry.Line`.

    Parameters
    ----------
    line : :class:`compas.geometry.Line`
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
    cgplane : :class:`compas.geometry.Plane`
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
    frame : :class:`compas.geometry.Frame`
        Frame to convert.

    Returns
    -------
    :class:`Rhino.Geometry.Plane`
        Resulting plane.
    """
    o = cgpoint_to_rgpoint(frame.point)
    x = cgvector_to_rgvector(frame.xaxis)
    y = cgvector_to_rgvector(frame.yaxis)
    return rg.Plane(o, x, y)


def matrix_to_rgtransform(M):
    """Create :class:`Rhino.Geometry.Transform` from a transformation matrix.

    Parameters
    ----------
    M : :class:`list` of :class:`list` of :class:`float`
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


def cgmesh_to_rgmesh(mesh):
    artist = MeshArtist(mesh)

    return artist.draw_mesh()


def _test_functions():
    # test cgpoint_to_rgpoint
    point = cgpoint_to_rgpoint(cg.Point(1, 2, 3))
    if point.Z != 3.0:
        raise Exception("cgpoint_to_rgpoint failed.")

    # test cgvector_to_rgvector
    vector = cgvector_to_rgvector(cg.Vector(5, 1, 9))
    if not vector.Unitize():
        raise Exception("cgvector_to_rgvector failed")

    # test cgline_to_rgline
    line = cgline_to_rgline(cg.Line([1, 2, 3], [3, 2, 1]))
    if line.Direction != rg.Vector3d(2, 0, -2):
        raise Exception("cgline_to_rgline failed")

    # test frame_to_plane
    plane = cgframe_to_rgplane(cg.Frame([1, 3, -1], [1, 1, 2], [0, 1, 1]))
    if not isinstance(plane.Normal, rg.Vector3d):
        raise Exception("cgframe_to_rgplane failed")

    # matrix_to_rgtransform
    R = cg.Rotation.from_basis_vectors([1, 2, 0], [2, 1, 3])
    if not isinstance(matrix_to_rgtransform(R), rg.Transform):
        raise Exception("matrix_to_rgtransform failed")


if __name__ == "__main__":
    _test_functions()
