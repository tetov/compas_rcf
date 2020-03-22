"""
******************************************************************************
compas_rcf.docker
******************************************************************************

.. currentmodule:: compas_rcf.docker

Docker commands
===============

.. autosummary::
    :toctree: generated/
    :nosignatures:

    compose_up
    compose_down

Included docker-compose files
=============================

ABB specific
------------

ABB driver
^^^^^^^^^^

.. note::
   Requires private docker image file ``abb-driver``.

This docker setup is divided into two ``docker-compose`` files, the ``abb-driver``
container requires restarts from time to time while ``ros-master`` and
``ros-bridge`` doesn't.

.. literalinclude:: ../../src/compas_rcf/docker/compose_files/abb/driver-base-docker-compose.yml
   :language: yaml
   :caption: ros-master & ros-bridge

.. literalinclude:: ../../src/compas_rcf/docker/compose_files/abb/driver-docker-compose.yml
   :language: yaml
   :caption: driver
"""  # noqa: E501
from .docker_cmds import *  # noqa: F401,F403
