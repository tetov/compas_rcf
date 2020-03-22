"""
********************************************************************************
compas_rcf
********************************************************************************

.. currentmodule:: compas_rcf

python module for MAS DFAB project Rapid Clay Formations

Fabrication data setup and configuration
----------------------------------------

.. toctree::
   :maxdepth: 3

   compas_rcf.fab_data

Robot system specific code
--------------------------

.. toctree::
   :maxdepth: 3

   compas_rcf.abb
   compas_rcf.ur

Tools
-----

.. toctree::
   :maxdepth: 3

   compas_rcf.docker
   compas_rcf.rhino
   compas_rcf.utils
"""
import os

HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))

# from https://smarie.github.io/python-getversion/#package-versioning-best-practices
try:
    # -- Distribution mode --
    # import from _version.py generated by setuptools_scm during release
    from ._version import version as __version__
except ImportError:
    try:
        # -- Source mode --
        # use setuptools_scm to get the current version from src using git
        from setuptools_scm import get_version

        __version__ = get_version(HOME)
    except ImportError:
        __version__ = "dev"

__author__ = "Anton T Johansson"
__copyright__ = "MAS DFAB 1920 students and tutors"
__license__ = "MIT License"
__email__ = "anton@tetov.se"

__all__ = ["HOME", "DATA", "DOCS", "TEMP", "__version__"]
