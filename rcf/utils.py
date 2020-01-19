import random

import Rhino.Geometry as rg

import compas.geometry as cg


def rand_vector(dimensions):
    '''
    https://stackoverflow.com/a/8453514
    '''
    v = [random.gauss(0, 1) for i in range(dimensions)]
    magnitude = sum(x**2 for x in v)**.5
    vector = [x / magnitude for x in v]
    if len(vector) > 3:
        for i in range(3 - len(vector)):
            vector += [0]

    vector = rg.Vector3d(*vector)

    vector.Unitize()

    return vector


def get_centroid(closed_crv):
    area_obj = rg.AreaMassProperties.Compute(closed_crv)
    return area_obj.Centroid


def remap_value(value, from_domain, to_domain):
    from_min, from_max = from_domain
    to_min, to_max = to_domain

    from_range = (from_max - from_min)
    to_range = (to_max - to_min)
    new_value = (((value - from_min) * to_range) / from_range) + to_min

    return new_value


def flatten_list(l):
    return [item for sublist in l for item in sublist]


def shift_list(seq, shift=1):
    """
    https://stackoverflow.com/a/29498813
    """
    return seq[-shift:] + seq[:-shift]


def list_elem_w_index_wrap(l, i):
    return l[i % len(l)]


#
# compas - rhino convenience functions


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

    >>> point = cgpoint_to_rgpoint(cg.Point(1, 2, 3))
    >>> point.Z
    3.0

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

    >>> vector = cgvector_to_rgvector(cg.Vector(5, 1, 9))
    >>> vector.Unitize()
    0.483368244522832,0.0966736489045664,0.870062840141097

    """
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

    >>> line = cgline_to_rgline(rg.Line([1, 2, 3], [1, 2, 3]))
    >>> line.Length
    2.82842712475

    """
    return rg.Line(cgpoint_to_rgpoint(line.start), cgpoint_to_rgpoint(line.end))


def frame_to_plane(frame):  # type: (cg.Frame) -> rg.Plane
    """Convenience function to convert a compas.geometry.Frame object to a
       Rhino.Geometry.Plane object

    Parameters
    ----------
    compas.geometry.Frame
        Frame to convert

    Returns
    -------
    Rhino.Geometry.Plane
        Resulting Plane

    >>> plane = frame_to_plane(cg.Frame([1, 3, -1], [1, 1, 2], [0,1,1]))
    >>> plane.Normal
    -0.577350269189626,-0.577350269189626,0.577350269189626

    """
    return rg.Plane(cgpoint_to_rgpoint(frame.point), cgvector_to_rgvector(frame.normal))


#
# rhino -> compas convenience functions


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

    >>> pt = rgpoint_to_cgpoint(rg.Point3d(3, 2, 1))
    >>> pt.data
    [3.0, 2.0, 1.0]

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

    >>> v = rgvector_to_cgvector(rg.Vector(3, 2, 1))
    >>> v.length
    3.74165738677

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

    >>> line = rgline_to_cgline(rg.Line(rg.Point3d(3, 2, 1), rg.Vector3d(1, 1, 0), 5.))
    >>> line.midpoint
    3.74165738677

    """
    return cg.Line(rgpoint_to_cgpoint(line.From), rgpoint_to_cgpoint(line.To))


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

    >>> frame = rgplane_to_cgframe(rg.Plane(rg.Point3d(1, 3, 2), rg.Vector3d(2, -1, 1)))
    >>> frame.quaternion
    Quaternion(0.713799, 0.462707, 0.285969, 0.441152)

    """
    return cg.Frame(rgpoint_to_cgpoint(plane.Origin), rgvector_to_cgvector(plane.XAxis),
                    rgvector_to_cgvector(plane.YAxis))


if __name__ == "__main__":

    # rhino -> compas convenience functions

    # frame_to_plane
    plane = frame_to_plane(cg.Frame([1, 3, -1], [1, 1, 2], [0, 1, 1]))
    print(plane.Normal)

    # cgpoint_to_rgpoint
    point = cgpoint_to_rgpoint(cg.Point(1, 2, 3))
    print(point.Z)

    # cgline_to_rgline
    line = cgline_to_rgline(cg.Line([1, 2, 3], [3, 2, 1]))
    print(line.Length)

    # cgvector_to_rgvector
    vector = cgvector_to_rgvector(cg.Vector(5, 1, 9))
    vector.Unitize()
    print(vector)

    # rhino -> compas convenience functions

    # rgpoint_to_cgpoint
    pt = rgpoint_to_cgpoint(rg.Point3d(3, 2, 1))
    print(pt.data)

    # rgvector_to_cgvector
    v = rgvector_to_cgvector(rg.Vector3d(3, 2, 1))
    print(v.length)

    # rgline_cgline
    line = rgline_to_cgline(rg.Line(rg.Point3d(3, 2, 1), rg.Vector3d(1, 1, 0), 5.))
    print(line.midpoint)

    # rgplane_to_cgframe
    frame = rgplane_to_cgframe(rg.Plane(rg.Point3d(1, 3, 2), rg.Vector3d(2, -1, 1)))
    print(frame.quaternion)

    # doctest doesn't in IronPython unless called on command line
    # import doctest
    # doctest.testmod()
