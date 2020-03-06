from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import Rhino.Geometry as rg


def get_centroid(closed_crv):
    area_obj = rg.AreaMassProperties.Compute(closed_crv)
    return area_obj.Centroid


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
