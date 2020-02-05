from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json

from compas_rcf.fabrication import ClayBullet


def load_bullets(file_path):

    with open(file_path, mode='r') as fp:
        json_string = json.load(fp)

    clay_bullets = []
    for dict_ in json_string:
        clay_bullets.append(ClayBullet.from_data(dict_))

    return clay_bullets
