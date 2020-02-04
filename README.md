# compas\_rcf

![Travis (.com)](https://img.shields.io/travis/com/tetov/compas_rcf?style=for-the-badge)
![GitHub](https://img.shields.io/github/license/tetov/compas_rcf?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/compas_rcf?style=for-the-badge)

python module for MAS DFAB project Rapid Clay Formations

## Example files

* [Grasshopper file setup with non interactive clay bullet placing with UR5.](https://github.com/tetov/compas_rcf/raw/master/docsource/examples/grasshopper_non_interactive.gh)

## Installation

### With [Anaconda](https://www.anaconda.com/)

1.  (Optional) set up environment if you don't have one with `compas_rrc`
    * `conda create -n compas_rcf python=3.7 git compas_fab`
    * `conda activate compas_rcf`
2.  Dependency [compas\_rrc](https://bitbucket.org/ethrfl/compas_rrc) is a private repository and needs to be installed first.
    * `pip install git+https://bitbucket.com/eth-rfl/compas_rrc`
    * Authentication problems? [Try this](#authentication-problems-with-bitbucket).
3.  Then install `compas_rcf`
    * `pip install compas_rcf` or `pip install compas_rcf==version` for specific version.
4.  Make package accessible in Rhino and Grasshopper `python -m compas_rcf.install_rhino`

### With pip

1.  (Optional) set up environment
2.  Dependency [compas\_rrc](https://bitbucket.org/ethrfl/compas_rrc) is a private repository and needs to be installed first.
    * `pip install git+https://bitbucket.com/eth-rfl/compas_rrc`
    * Authentication problems? [Try this](#authentication-problems-with-bitbucket).
3.  Then install `compas_rcf`
    * `pip install compas_rcf` or `pip install compas_rcf==version` for specific version.
4.  Make package accessible in Rhino and Grasshopper `python -m compas_rcf.install_rhino`

## Installation if you want work on the code

###  With Anaconda

1.  (Optional) set up environment
    -   `conda create -n compas_rcf-dev python=3.7 git compas_fab`
    -   `conda activate compas_rcf-dev`
2.  Dependency [compas\_rrc](https://bitbucket.org/ethrfl/compas_rrc) is a private repository and needs to be installed first.
    -   `pip install git+https://bitbucket.com/eth-rfl/compas_rrc`
    -   Alternatively you can install it from a directory if you need to make changes:
        -   `cd /path/to/repository/directory`
        -   `git clone https://bitbucket.com/eth-rfl/compas_rrc`
        -   `pip install -e compas_rrc`
        -   You can run the last command in a folder you have cloned using another git client (like SourceTree)
    - Authentication problems? [Try this](#authentication-problems-with-bitbucket).
3.  Then install `compas_rcf`
    -   `cd /path/to/repository/directory`
    -   `git clone https://github.com/tetov/compas_rcf`
    -   `pip install -e compas_rcf`
    -   Same goes here, you can run this in a folder cloned with SourceTree
4.  Make package accessible in Rhino and Grasshopper `python -m compas_rcf.install_rhino`

### With pip

1.  (Optional) set up environment
2.  Dependency [compas\_rrc](https://bitbucket.org/ethrfl/compas_rrc) is a private repository and needs to be installed first.
    -   `pip install git+https://bitbucket.com/eth-rfl/compas_rrc`
    -   Alternatively you can install it from a directory if you need to make changes:
        -   `cd /path/to/repository/directory`
        -   `git clone https://bitbucket.com/eth-rfl/compas_rrc`
        -   `pip install -e compas_rrc`
    - Authentication problems? [Try this](#authentication-problems-with-bitbucket).
3.  Then install `compas_rcf`
    -   `cd /path/to/repository/directory`
    -   `git clone https://github.com/tetov/compas_rcf`
    -   `pip install -e compas_rcf`
4.  Make package accessible in Rhino and Grasshopper `python -m compas_rcf.install_rhino`

## Update installation

Run this command in your environment:
`pip install -U git+https://github.com/tetov/compas_rcf`

If you are running the package from latest commit, git pull would achieve the same. If requirements have changed you will need to run `pip install -e .`.

## Known issues

### Authentication problems with BitBucket

Git authentication works so so on Windows. Try installing the new the new [Git Credential Manager for Windows](https://github.com/Microsoft/Git-Credential-Manager-for-Windows/releases/latest) and authenticating with that.
