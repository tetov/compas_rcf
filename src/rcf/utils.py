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


def remap_values(values, from_domain, to_domain, include_clipped=False):
    # TODO: Debug (reverse values compared to remap values in gh)
    from_min, from_max = from_domain
    to_min, to_max = to_domain

    from_range = (from_max - from_min)
    to_range = (to_max - to_min)

    remapped_values = []

    if not hasattr(values, "__iter__"):
        values = [values]

    for value in values:
        new_value = (((value - from_min) * to_range) / from_range) + to_min

        if to_min < new_value < to_max:
            remapped_values.append(new_value)

        elif include_clipped:
            remapped_values.append(new_value)

    if len(remapped_values) == 1:
        return remapped_values[0]
    else:
        return remapped_values


def flatten_list(l):
    return [item for sublist in l for item in sublist]


def shift_list(seq, shift=1):
    """
    https://stackoverflow.com/a/29498813
    """
    return seq[-shift:] + seq[:-shift]


def list_elem_w_index_wrap(l, i):
    return l[i % len(l)]


def flip_matrix(listlike):
    """Rotate 2D-array

    Parameters
    ----------
    listlike: iterable
        array to rotate

    Returns
    -------
    iterable
        rotated array

    Notes
    -----
    Taken from https://stackoverflow.com/a/496056
    """
    return zip(*listlike[::-1])


def axis_angle_vector_from_plane_to_plane(plane_to, plane_from=rg.Plane.WorldXY):
    T = rg.Transform.PlaneToPlane(plane_from, plane_to)
    M = rgtransform_to_matrix(T)
    return cg.axis_angle_vector_from_matrix(M)


def reparametrize_crvs(crv_or_crvs, domain=(0, 1)):
    interval = rg.Interval(*domain)
    new_crvs = []

    if not isinstance(crv_or_crvs, list):
        got_list = False
        crv_or_crvs = list(crv_or_crvs)
    else:
        got_list = True

    new_crvs = [crv.DuplicateCurve() for crv in crv_or_crvs]

    for crv in new_crvs:
        crv.Domain = interval

    if not got_list:
        return new_crvs[1]
    else:
        return new_crvs


#
# compas_rhino.artists
# compas to rhino convenience functions


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


#
# compas_rhino.constructors
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


#
# rg.Transform <-> python matrix (list of lists)


def rgtransform_to_matrix(rgM):
    M = [[rgM.Item[i, j] for j in range(4)] for i in range(4)]
    return M


def matrix_to_rgtransform(M):
    rgM = rg.Transform()
    for i, row in enumerate(M):
        for j, val in enumerate(row):
            rgM[i, j] = val
    return rgM


#
# Fun IronPython conversions


def array_to_list(array):
    return list(array)


def list_of_arrays_to_list_of_lists(list_of_arrays):
    list_of_lists = []
    for array in list_of_arrays:
        list_of_lists.append(array_to_list(array))
    return list_of_lists


if __name__ == "__main__":

    # rhino -> compas convenience functions

    # cgpoint_to_rgpoint
    point = cgpoint_to_rgpoint(cg.Point(1, 2, 3))
    assert point.Z == 3.0

    # cgvector_to_rgvector
    vector = cgvector_to_rgvector(cg.Vector(5, 1, 9))
    assert vector.Unitize() is True

    # cgline_to_rgline
    line = cgline_to_rgline(cg.Line([1, 2, 3], [3, 2, 1]))
    assert line.Direction == rg.Vector3d(2, 0, -2)

    # frame_to_plane
    plane = cgframe_to_rgplane(cg.Frame([1, 3, -1], [1, 1, 2], [0, 1, 1]))
    assert isinstance(plane.Normal, rg.Vector3d)

    # rhino -> compas convenience functions

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

    # matrix_to_rgtransform
    R = cg.Rotation.from_basis_vectors([1, 2, 0], [2, 1, 3])
    assert isinstance(matrix_to_rgtransform(R), rg.Transform)
