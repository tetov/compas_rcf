"""
********************************************************************************
rapid_clay_formations_fab.fab_data
********************************************************************************

.. currentmodule:: rapid_clay_formations_fab.fab_data

"""


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas import IPY

from .fabrication_element import *  # noqa: F401,F403

if not IPY:
    from .fab_conf import *  # noqa: F401,F403
