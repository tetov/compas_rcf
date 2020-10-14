*****************************************************************************
Installation
*****************************************************************************

Install
=======

.. note::
    All code related to fabrication with ABB industrial robots requires
    `compas_rrc <https://bitbucket.org/ethrfl/compas_rrc/>`__ which is hosted in a private repository.

#.  Create a virtual environment using your tool of choice
    (e.g. ``virtualenv``, ``conda``, etc).

    -  Using `Anaconda <https://www.anaconda.com/>`__

    .. code:: bash

       conda config --add channels conda-forge
       # use conda to install compas_fab if possible
       conda create -n rapid_clay_formations_fab python=3.8 git compas_fab==0.11
       conda activate rapid_clay_formations_fab

    -  Using `virtualenv <https://github.com/pypa/virtualenv>`__

    .. code:: bash

       virtualenv --python=python3.8 {{path/to/venv}}
       source {{path/to/venv}}/bin/activate

#.  Install ``compas_rrc`` & ``rapid_clay_formations_fab``

    .. code:: bash

       # install compas_rrc separately
       pip install git+https://bitbucket.org/ethrfl/compas_rrc@v1.0.0
       # from latest commit on git
       pip install git+https://github.com/gramaziokohler/rapid_clay_formations_fab
       # or last version
       pip install rapid_clay_formations_fab
       # or specific version
       rapid_clay_formations_fab=={version}

    If you have authentication issues with BitBucket (for compas_rrc), see :ref:`git_cred_windows`

#.  Make package accessible in Rhino and Grasshopper

    .. code:: bash

       python -m rapid_clay_formations_fab.rhino.install

Update
======

To update the repository run:

.. code:: bash

   pip install -U rapid_clay_formations_fab
   # or if you installed directly from github
   pip install -U git+https://github.com/gramaziokohler/rapid_clay_formations_fab
