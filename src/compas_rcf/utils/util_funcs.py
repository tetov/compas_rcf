from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import random

import Rhino.Geometry as rg


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


def array_to_list(array):
    return list(array)


def list_of_arrays_to_list_of_lists(list_of_arrays):
    list_of_lists = []
    for array in list_of_arrays:
        list_of_lists.append(array_to_list(array))
    return list_of_lists
