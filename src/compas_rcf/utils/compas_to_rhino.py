"""Most of these are in compas >=0.15 but compas_fab is not there yet
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.geometry as cg

from compas_rcf import IPY

if IPY:
    import Rhino.Geometry as rg


def cgpoint_to_rgpoint(pt):  # type: (cg.Point) -> rg.Point3d
    """Convenience function to convert a compas.geometry.Point object to the
       corresponding COMPAS object

    Parameters
    ----------
    compas.geometry.Point
        Point object to convert

    Returns
    -------
    Rhino.Geometry.Point3d
        Resulting Point3d object
    """
    return rg.Point3d(*pt.data)


def cgvector_to_rgvector(v):  # type: (cg.Vector) -> rg.Vector3d
    """Convenience function to convert a compas.geometry.Vector object to the
       corresponding COMPAS object

    Parameters
    ----------
    compas.geometry.Vector
        Vector object to convert

    Returns
    -------
    Rhino.Geometry.Vector3d
        Resulting Vector3d object
    """
    # TODO: Implement in compas
    return rg.Vector3d(*v.data)


def cgline_to_rgline(line):  # type: (cg.Line) -> rg.Line
    """Convenience function to convert a compas.geometry.Line object to the
       corresponding COMPAS object

    Parameters
    ----------
    compas.geometry.Line
        Point object to convert

    Returns
    -------
    Rhino.Geometry.Line
        Resulting Line object
    """
    return rg.Line(cgpoint_to_rgpoint(line.start), cgpoint_to_rgpoint(line.end))


def cgplane_to_rgplane(cgplane):  # type: (cg.Plane) -> rg.Plane
    """Convenience function to convert a compas.geometry.Plane object to the
       corresponding Rhino.Geometry object
    Parameters
    ----------
    compas.geometry.Plane
        Plane to convert
    Returns
    -------
    Rhino.Geometry.Plane
        Resulting plane
    """
    return rg.Plane(cgpoint_to_rgpoint(cgplane.point), cgvector_to_rgvector(cgplane.normal))


def cgframe_to_rgplane(frame):  # type: (cg.Frame) -> rg.Plane
    """Convenience function to convert a compas.geometry.Frame object to a
       Rhino.Geometry.Plane object
    Parameters
    ----------
    compas.geometry.Frame
        Frame to convert
    Returns
    -------
    Rhino.Geometry.Plane
        Resulting plane
    """
    plane = cg.Plane(frame.point, frame.normal)
    return cgplane_to_rgplane(plane)


def matrix_to_rgtransform(M):
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
