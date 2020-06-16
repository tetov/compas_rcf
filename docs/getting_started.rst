*****************************************************************************
Getting started
*****************************************************************************

Installation
============

.. note::
    All code related to fabrication with ABB industrial robots requires
    `compas_rrc <https://bitbucket.org/ethrfl/compas_rrc/>`__ which is hosted in a private repository.

#.  (Optional) Create a virtual environment using your tool of choice
    (e.g. ``virtualenv``, ``conda``, etc).

    -  Using `Anaconda <https://www.anaconda.com/>`__

    .. code:: bash

       conda config --add channels conda-forge
       # use conda to install compas_fab if possible
       conda create -n compas_rcf python=3.7 git compas_fab
       conda activate compas_rcf

    -  Using `virtualenv <https://github.com/pypa/virtualenv>`__

    .. code:: bash

       virtualenv --python=python3.7 {{path/to/venv}}
       source {{path/to/venv}}/bin/activate

#.  Install ``compas_rrc`` & ``compas_rcf``

    .. code:: bash

       # install compas_rrc separately
       pip install git+https://bitbucket.org/ethrfl/compas_rrc#egg=compas_rrc-v0.2.2
       pip install compas_rcf
       # or compas_rcf=={version} for specific version

    If you have authentication issues with BitBucket (for compas_rrc), see :ref:`git_cred_windows`

#.  (Optional) Make package accessible in Rhino and Grasshopper

    .. code:: bash

       python -m compas_rcf.rhino.install

Update
======

To update the repository run:

.. code:: bash

   pip install -U compas_rcf
