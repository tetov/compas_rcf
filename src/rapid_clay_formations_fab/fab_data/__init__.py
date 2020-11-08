"""
********************************************************************************
rapid_clay_formations_fab.fab_data
********************************************************************************

.. currentmodule:: rapid_clay_formations_fab.fab_data


Fabrication datastructures
--------------------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

Fabrication configuration
-------------------------

Some fabrication settings can be set while running
:any:`rapid_clay_formations_fab.abb.run` but most are set before a run in YAML
format. Here is the default config:

.. literalinclude:: ../../src/rapid_clay_formations_fab/fab_data/config_default.yaml
   :language: yaml

.. autosummary::
    :toctree: generated/
    :nosignatures:

Tools & Utilities
-----------------

.. autosummary::
    :toctree: generated/
    :nosignatures:
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas import IPY

from .fabrication_element import *  # noqa: F401,F403

if not IPY:
    from .fab_conf import *  # noqa: F401,F403
