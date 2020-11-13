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

import pkgutil
from typing import List

from compas_rhino import install

STD_PKGS = ("compas_fab", "roslibpy", "rapid_clay_formations_fab", "compas_rrc")

# OPTIONAL_PKGS = ["couchdb"]
OPTIONAL_PKGS: List[str] = []

INSTALLED_PKGS = [mod.name for mod in list(pkgutil.iter_modules())]


def install_pkgs_to_rhino(*args):
    pkgs = set(install.INSTALLABLE_PACKAGES)

    for pkg in STD_PKGS:
        if pkg not in INSTALLED_PKGS:
            raise RuntimeError("Required package {} is not installed.".format(pkg))
        pkgs.add(pkg)

    for pkg in OPTIONAL_PKGS:
        if pkg in INSTALLED_PKGS:
            pkgs.add(pkg)
        else:
            print(f"Skipping {pkg} since it's not installed in current environment.")

    install.install(version="6.0", packages=pkgs)


if __name__ == "__main__":
    install_pkgs_to_rhino()
