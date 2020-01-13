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
