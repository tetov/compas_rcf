# Contributing

Contributions are welcome and very much appreciated!

## Code contributions

We accept code contributions through pull requests.
In short, this is how that works.

### Setup

**Important:** All code related to fabrication with ABB industrial robots requires [compas_rrc](https://bitbucket.org/ethrfl/compas_rrc/) which is hosted in a private repository.

1. Fork [the repository](https://github.com/gramaziokohler/rapid_clay_formations_fab) and clone the fork.

2. Create a virtual environment using your tool of choice (e.g. `virtualenv`, `conda`, etc).

    * Using [Anaconda](https://www.anaconda.com/)

    ```bash
    conda config --add channels conda-forge
    # use conda to install compas_fab if possible
    conda create -n rapid_clay_formations_fab-dev python=3.7 git compas_fab
    conda activate rapid_clay_formations_fab-dev
    ```

    * Using [virtualenv](https://github.com/pypa/virtualenv)

    ```bash
    virtualenv --python=python3.7 {{path/to/venv}}
    source {{path/to/venv}}/bin/activate
    ```

3. Install package and dependencies:

   ```bash
   cd path/to/rapid_clay_formations_fab
   pip install git+https://bitbucket.org/ethrfl/compas_rrc@v1.0.0
   pip install -e .[dev]
   ```

   If you have authentication issues with BitBucket (for `compas_rrc`) [Try installing
   the new Git Credential manager for Windows](https://gramaziokohler.github.io/rapid_clay_formations_fab/known_issues.html)

4. (Optional) Make package accessible in Rhino and Grasshopper

   ```bash
   python -m rapid_clay_formations_fab.rhino.install
   ```

### Make a pull request

1. Make sure all tests pass on the unmodified code:

   ```bash
   invoke test
   ```

2. Start making your changes to the **master** branch (or branch off of it) on your fork.
3. Make sure all tests still pass:

   ```bash
   invoke test
   ```

4. Add yourself to the *Contributors* section of `AUTHORS.md`.
5. Document the changes in the `CHANGELOG.md`
6. Commit your changes and push your branch to GitHub.
7. Create a [pull request](https://help.github.com/articles/about-pull-requests/) through the GitHub website.

During development, use [pyinvoke](http://docs.pyinvoke.org/) tasks on the
command line to ease recurring operations:

* `invoke clean`: Clean all generated artifacts.
* `invoke check`: Run various code and documentation style checks.
* `invoke docs`: Generate documentation.
* `invoke test`: Run all tests and checks in one swift command.
* `invoke`: Show available tasks.

## Bug reports

When [reporting a bug](https://github.com/gramaziokohler/rapid_clay_formations_fab/issues) please include:

* Operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

## Feature requests

When [proposing a new feature](https://github.com/gramaziokohler/rapid_clay_formations_fab/issues) please include:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
