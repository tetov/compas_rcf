"""Utility functions."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas.geometry as cg
from compas import IPY

if IPY:
    import Rhino.Geometry as rg
    from compas_rcf.rhino import rgplane_to_cgframe
    from compas_rcf.rhino import rgpoint_to_cgpoint


def wrap_list(list_, idx):
    """Return value at index, wrapping if necessary.

    Parameters
    ----------
    list_ : :class:`list`
        List to wrap around.
    idx : :class:`int`
        Index of item to return in list.

    Returns
    -------
    :class:`list` element
        Item at given index, index will be wrapped if necessary.
    """
    return list_[idx % len(list_)]


def ensure_frame(frame_like):
    """Convert geometry objects to :class:`compas.geometry.Frame`.

    Parameters
    ----------
    frame_like
        Frame like object, currently :class:`compas.geometry.Frame`,
        :class:`compas.geometry.Plane`, :class:`compas.geometry.Point`,
        :class:`Rhino.Geometry.Plane`, or :class:`Rhino.Geometry.Point3d`.

    Returns
    -------
    :class:`compas.geometry.Frame`

    Notes
    -----
    If a point is given the point is used as the frames origin and the X and
    Y will be the X and Y unit vectors.

    :class:`compas.geometry.Plane` is defined only by origin and normal, the
    X and Y axis will be chosen arbitrarely,
    see :meth:`compas.geometry.Frame.from_plane`.
    """
    if isinstance(frame_like, cg.Frame):
        return frame_like

    if isinstance(frame_like, cg.Plane):
        return cg.Frame.from_plane(frame_like)

    if isinstance(frame_like, cg.Point):
        return cg.Frame(frame_like, [1, 0, 0], [0, 1, 0])

    if IPY:
        if isinstance(frame_like, rg.Plane):
            return rgplane_to_cgframe(frame_like)
        if isinstance(frame_like, rg.Point3d):
            pt = rgpoint_to_cgpoint(frame_like)
            return cg.Frame(pt, [1, 0, 0], [0, 1, 0])

    raise TypeError(
        "Can't convert {} to compas.geometry.Frame".format(type(frame_like))
    )


def get_offset_frame(frame, distance):
    """Offset a frame in its reverse Z axis direction.

    Parameters
    ----------
    frame : :class:`compas.geometry.Frame`
        Frame to offset.
    distance : :class:`float`
        Translation distance in mm.

    Returns
    -------
    :class:`compas.geometry.Frame`
    """
    offset_vector = frame.zaxis * distance * -1
    T = cg.Translation(offset_vector)

    return frame.transformed(T)
