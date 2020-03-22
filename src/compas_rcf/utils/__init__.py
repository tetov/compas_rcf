"""
********************************************************************************
compas_rcf.utils
********************************************************************************

.. currentmodule:: compas_rcf.utils

UI utilities
============

.. autosummary::
    :toctree: generated/

    open_file_dialog

General utilities
=================

.. autosummary::
    :toctree: generated/

    wrap_list
    ensure_frame
    get_offset_frame
"""
from compas import IPY

from .util_funcs import *  # noqa: F401,F403

if not IPY:
    from .ui import *  # noqa: F401,F403
