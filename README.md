# rcf

python module for MAS DFAB project Rapid Clay Formations

## Installation

1.  Set up a new [Anaconda](https://www.anaconda.com/) environment (skip to step 3 if you have a environment with `compas_rrc` and Python 3)
    -   `conda create -n mast2p1 --python=3.7 git --yes`
    -   `conda activate mast2p1`
2.  Dependency [compas\_rrc](https://bitbucket.org/ethrfl/compas_rrc) is a private repository and needs to be installed first.
    -   `pip install git+https://bitbucket.com/eth-rfl/compas_rrc`
    -   If you have trouble authenticating try to clone the repository to a folder and while in that folder run `pip install -e .`
3.  Install this package next (might change to pypi or conda install)
    -   `pip install git+https://github.com/tetov/rcf@v0.1.0#egg=rcf`
    -   If you have trouble installing compas or compas\_fab you can run `conda install compas_fab'>=0.10.1,<0.12' --yes` and then try again
