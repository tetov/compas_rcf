"""
********************************************************************************
compas_rcf.fab_data
********************************************************************************

.. currentmodule:: compas_rcf.fab_data


Fabrication datastructures
--------------------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ClayBullet
    ClayStructure

Fabrication configuration
-------------------------

Some fabrication settings can be set while running :any:`compas_rcf.abb.run`
but most are set before a run in YAML format. Here is the default config:

.. literalinclude:: ../../src/compas_rcf/fab_data/config_default.yaml
   :language: yaml

.. autosummary::
    :toctree: generated/
    :nosignatures:

    interactive_conf_setup

Tools & Utilities
-----------------

.. autosummary::
    :toctree: generated/
    :nosignatures:

    csv_reports
    load_bullets
    ClayBulletEncoder
    check_id_collision
"""
from compas import IPY

from .clay_objs import *  # noqa: F401,F403
from .csv_report import *  # noqa: F401,F403
from .tools import *  # noqa: F401,F403

if not IPY:
    from .conf import *  # noqa: F401,F403
