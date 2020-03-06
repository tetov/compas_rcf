"""
********************************************************************************
compas_rcf.rhino
********************************************************************************

.. currentmodule:: compas_rcf.rhino

Rhino package installer
-----------------------
`compas_rcf.rhino.install` installs compas, compas_fab, roslibpy, compas_rrc and
compas_rcf to Rhino's IronPython lib directory using compas installer.

RhinoCommon to COMPAS object conversions
----------------------------------------
Scripts for converting geometry objects between the two frameworks. Most of this
has been integrated into COMPAS v0.15.0 but compas_fab needs earlier versions
of COMPAS.
"""
from compas import IPY

if IPY:
    from .compas_to_rhino import *  # noqa: F401,F403
    from .rhino_to_compas import *  # noqa: F401,F403
    from .rhino_utils import *  # noqa: F401,F403
