from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_rhino import install

PACKAGES = ["compas_fab", "roslibpy", "compas_rcf", "compas_rrc"]


if __name__ == "__main__":

    packages = set(install.INSTALLABLE_PACKAGES + PACKAGES)

    install.install(version="6.0", packages=packages)
