"""
********************************************************************************
rapid_clay_formations_fab.rhino
********************************************************************************

.. currentmodule:: rapid_clay_formations_fab.rhino

Rhino package installer
=======================
``rapid_clay_formations_fab.rhino.install`` installs
`compas <https://compas-dev.github.io/>`_,
`compas_fab <https://gramaziokohler.github.io/compas_fab>`_,
`roslibpy <https://roslibpy.readthedocs.io/>`_,
`compas_rrc <https://bitbucket.org/ethrfl/compas_rrc/>`_ and
``rapid_clay_formations_fab`` to Rhino's script directory using the
``compas_rhino`` installer.

Usage: ``python -m rapid_clay_formations_fab.rhino.install``

RhinoCommon to COMPAS object conversions and other utilities
============================================================

:mod:`rapid_clay_formations_fab.rhino.rhino_to_compas` and
:mod:`rapid_clay_formations_fab.rhino.compas_to_rhino` contains conversion
functions between the two frameworks.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas import RHINO

if RHINO:
    from .compas_to_rhino import *  # noqa: F401,F403
    from .rhino_to_compas import *  # noqa: F401,F403
