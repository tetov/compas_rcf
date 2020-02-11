"""
********************************************************************************
compas_rcf.fabrication
********************************************************************************

.. currentmodule:: compas_rcf.fabrication

Runners & fabrication objects
-----------------------------
This modules contains runners; scripts for running a fabrication process using a
digital fabrication method. It also contains fabrication objects, most significantly
:class:`compas_rcf.fabrication.ClayBullet` which is our data representation of our
discrete building blocks.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .clay_obj import *  # noqa: F401,F403
from .network import *  # noqa: F401,F403
