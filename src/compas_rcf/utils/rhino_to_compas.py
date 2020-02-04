"""Most of these are in compas >=0.15 but compas_fab is not there yet
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.geometry as cg
import Rhino.Geometry as rg


def rgpoint_to_cgpoint(pt):  # type: (rg.Point3d) -> cg.Point
    """Convenience function to convert Rhino.Geometry.Point3d object to the
       corresponding COMPAS object

    Parameters
    ----------
    Rhino.Geometry.Point3d
        Plane object to convert

    Returns
    -------
    compas.geometry.Point
        Resulting point object
    """
    return cg.Point(pt.X, pt.Y, pt.Z)


def rgvector_to_cgvector(v):  # type: (rg.Point3d) -> cg.Vector
    """Convenience function to convert Rhino.Geometry.Vector3d object to the
       corresponding COMPAS object

    Parameters
    ----------
    Rhino.Geometry.Vector3d
        Vector object to convert

    Returns
    -------
    compas.geometry.Vector
        Resulting vector object
    """
    return cg.Vector(v.X, v.Y, v.Z)


def rgline_to_cgline(line):  # type: (rg.Line) -> cg.Line
    """Convenience function to convert Rhino.Geometry.Line object to the
       corresponding COMPAS object

    Parameters
    ----------
    Rhino.Geometry.Line
        Line object to convert

    Returns
    -------
    compas.geometry.Line
        Resulting line object
    """
    return cg.Line(rgpoint_to_cgpoint(line.From), rgpoint_to_cgpoint(line.To))


def rgplane_to_cgplane(plane):  # type: (rg.Plane) -> cg.Plane
    """Convenience function to convert Rhino.Geometry.Plane object to the
       corresponding compas.geometry object
    Parameters
    ----------
    Rhino.Geometry.Plane
        Plane object to convert
    Returns
    -------
    compas.geometry.Plane
        Resulting plane object
    """
    return cg.Plane(rgpoint_to_cgpoint(plane.Origin), rgvector_to_cgvector(plane.Normal))


def rgplane_to_cgframe(plane):  # type: (rg.Plane) -> cg.Frame
    """Convenience function to convert Rhino.Geometry.Plane object to a
       compas.geometry.Frame object
    Parameters
    ----------
    Rhino.Geometry.Plane
        Plane object to convert
    Returns
    -------
    compas.geometry.Frame
        Resulting frame object
    """
    cgplane = rgplane_to_cgplane(plane)
    return cg.Frame.from_plane(cgplane)


def rgtransform_to_matrix(rgM):
    M = [[rgM.Item[i, j] for j in range(4)] for i in range(4)]
    return M


if __name__ == "__main__":

    # rgpoint_to_cgpoint
    pt = rgpoint_to_cgpoint(rg.Point3d(3, 2, 1))
    assert pt.data == [3.0, 2.0, 1.0]

    # rgvector_to_cgvector
    v = rgvector_to_cgvector(rg.Vector3d(3, 2, 1))
    assert v.length > 3.7 and v.length < 3.8

    # rgline_cgline
    line = rgline_to_cgline(rg.Line(rg.Point3d(3, 2, 1), rg.Vector3d(1, 1, 0), 5.))
    assert isinstance(line.midpoint.z, float)

    # rgplane_to_cgframe
    frame = rgplane_to_cgframe(rg.Plane(rg.Point3d(1, 3, 2), rg.Vector3d(2, -1, 1)))
    frame.quaternion.__repr__ == 'Quaternion(0.713799, 0.462707, 0.285969, 0.441152)'

    # rgtransform_to_matrix
    matrix = rg.Transform.ZeroTransformation
    assert rgtransform_to_matrix(matrix) == [[0., 0., 0., 0.], [0., 0., 0., 0.], [0., 0., 0., 0.], [0., 0., 0., 1.]]
