# compas\_rcf

python module for MAS DFAB project Rapid Clay Formations

## Installation

### With [Anaconda](https://www.anaconda.com/)

1.  (Optional) set up environment `conda create -n compas_rcf python=3.7 git`
2.  Dependency [compas\_rrc](https://bitbucket.org/ethrfl/compas_rrc) is a private repository and needs to be installed first. `pip install git+https://bitbucket.com/eth-rfl/compas_rrc`
3.  Then install `compas_rcf` `conda install compas_rcf` or `conda install compas_rcf=version` for specific version.
4.  Make package accessible in Rhino and Grasshopper `python -m compas_rcf.install_rhino`

### With pip

1.  (Optional) set up environment
2.  Dependency [compas\_rrc](https://bitbucket.org/ethrfl/compas_rrc) is a private repository and needs to be installed first. `pip install git+https://bitbucket.com/eth-rfl/compas_rrc`
3.  Then install `compas_rcf` `pip install compas_rcf` or `pip install compas_rcf==version` for specific version.
4.  Make package accessible in Rhino and Grasshopper `python -m compas_rcf.install_rhino`

## Installation for contributors

### With Anaconda

1.  (Optional) set up environment
    -   `conda create -n compas_rcf-dev python=3.7 git`
2.  Dependency [compas\_rrc](https://bitbucket.org/ethrfl/compas_rrc) is a private repository and needs to be installed first.
    -   `pip install git+https://bitbucket.com/eth-rfl/compas_rrc`
    -   Alternatively you can install it from a directory if you need to make changes:
        -   `cd /path/to/repository/directory`
        -   `git clone https://bitbucket.com/eth-rfl/compas_rrc`
        -   `pip install -e compas_rrc`
3.  Then install `compas_rcf`
    -   `cd /path/to/repository/directory`
    -   `git clone https://github.com/tetov/compas_rcf`
    -   `pip install -e compas_rcf`
4.  Make package accessible in Rhino and Grasshopper `python -m compas_rcf.install_rhino`

### With pip

1.  (Optional) set up environment
2.  Dependency [compas\_rrc](https://bitbucket.org/ethrfl/compas_rrc) is a private repository and needs to be installed first.
    -   `pip install git+https://bitbucket.com/eth-rfl/compas_rrc`
    -   Alternatively you can install it from a directory if you need to make changes:
        -   `cd /path/to/repository/directory`
        -   `git clone https://bitbucket.com/eth-rfl/compas_rrc`
        -   `pip install -e compas_rrc`
3.  Then install `compas_rcf`
    -   `cd /path/to/repository/directory`
    -   `git clone https://github.com/tetov/compas_rcf`
    -   `pip install -e compas_rcf`
4.  Make package accessible in Rhino and Grasshopper `python -m compas_rcf.install_rhino`
