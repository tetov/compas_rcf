"""
********************************************************************************
compas_rcf
********************************************************************************

.. currentmodule:: compas_rcf


.. toctree::
    :maxdepth: 1


"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import compas

__author__ = ["Anton T Johansson"]
__copyright__ = "MAS DFAB 1920 students and tutors"
__license__ = "MIT License"
__email__ = "anton@tetov.se"
__version__ = "0.1.4"


HERE = os.path.dirname(__file__)

HOME = os.path.abspath(os.path.join(HERE, "../../"))
DATA = os.path.abspath(os.path.join(HOME, "data"))
DOCS = os.path.abspath(os.path.join(HOME, "docs"))
TEMP = os.path.abspath(os.path.join(HOME, "temp"))

# Check if package is installed from git
# If that's the case, try to append the current head's hash to __version__
try:
    git_head_file = compas._os.absjoin(HOME, '.git', 'HEAD')

    if os.path.exists(git_head_file):
        # git head file contains one line that looks like this:
        # ref: refs/heads/master
        with open(git_head_file, 'r') as git_head:
            _, ref_path = git_head.read().strip().split(' ')
            ref_path = ref_path.split('/')

            git_head_refs_file = compas._os.absjoin(HOME, '.git', *ref_path)

        if os.path.exists(git_head_refs_file):
            with open(git_head_refs_file, 'r') as git_head_ref:
                git_commit = git_head_ref.read().strip()
                __version__ += '-' + git_commit[:8]
except Exception:
    pass

__all__ = ["HOME", "DATA", "DOCS", "TEMP"]
