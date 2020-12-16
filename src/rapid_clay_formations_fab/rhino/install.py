"""
******************************************************************************
rapid_clay_formations_fab.rhino.install
******************************************************************************

Installs ``rapid_clay_formations_fab`` and its dependencies to the Rhino
IronPython environment.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_rhino import install

NON_PLUGINS = ["compas_rrc", "rapid_clay_formations_fab"]


def install_pkgs_to_rhino(*args):

    # Install compas and installable_rhino_package plugins
    install.install(version="6.0")

    # Install packages "manually"
    install.install(version="6.0", packages=NON_PLUGINS)


if __name__ == "__main__":
    install_pkgs_to_rhino()
