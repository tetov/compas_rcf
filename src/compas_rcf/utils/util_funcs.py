from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import random

import compas.geometry as cg
from compas import IPY

if IPY:
    import Rhino.Geometry as rg
    from compas_rcf.utils.rhino_to_compas import rgplane_to_cgframe
    from compas_rcf.utils.rhino_to_compas import rgpoint_to_cgpoint


def rand_vector(dimensions):
    """Create a random vector.

    Pads vector if fewer than three dimensions up to three dimensions.

    Parameters
    ----------
    dimensions : int

    Returns
    -------
    `class`:compas.geometry.Vector
        Unitized random vector

    Notes
    -----
    Adapted from `Stack Overflow <https://stackoverflow.com/a/8453514>`_
    """
    v = [random.gauss(0, 1) for i in range(dimensions)]
    magnitude = sum(x ** 2 for x in v) ** 0.5
    vector = [x / magnitude for x in v]
    if len(vector) < 3:
        for i in range(3 - len(vector)):
            vector += [0]

    vector = cg.Vector(vector)

    vector.unitize()

    return vector


def remap_values(values, from_domain, to_domain, include_clipped=False):
    # TODO: Debug (reverse values compared to remap values in gh)
    from_min, from_max = from_domain
    to_min, to_max = to_domain

    from_range = from_max - from_min
    to_range = to_max - to_min

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
    """Shift indices of list, wrapping at end.

    Notes
    -----
    Source: https://stackoverflow.com/a/29498813
    """
    return seq[-shift:] + seq[:-shift]


def list_elem_w_index_wrap(l, i):
    return l[i % len(l)]


def flip_matrix(listlike):
    """Rotate 2D-array.

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


def ensure_frame(frame_like):
    if isinstance(frame_like, cg.Frame):
        return frame_like

    if isinstance(frame_like, cg.Plane):
        return cg.Frame.from_plane(frame_like)

    if IPY:
        if isinstance(frame_like, rg.Plane):
            return rgplane_to_cgframe(frame_like)
        if isinstance(frame_like, rg.Point3d):
            pt = rgpoint_to_cgpoint(frame_like)
            return cg.Frame(pt, cg.Vector(0, 1, 0), cg.Vector(1, 0, 0))

    raise TypeError(
        "Can't convert {} to compas.geometry.Frame".format(type(frame_like))
    )


def get_offset_frame(frame, distance):
    """Offset a frame in its Z axis direction.

    Parameters
    ----------
    frame : `class`:compas.geometry.Frame
        Frame to offset
    distance : float
        Translation distance in mm

    Returns
    -------
    `class`:compas.geometry.Frame
    """
    offset_vector = frame.zaxis * distance * -1
    T = cg.Translation(offset_vector)

    return frame.transformed(T)
