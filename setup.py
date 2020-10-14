#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import io
from os import path

from setuptools import find_packages
from setuptools import setup

here = path.abspath(path.dirname(__file__))


def _read(*names, **kwargs):
    return io.open(
        path.join(here, *names), encoding=kwargs.get("encoding", "utf8")
    ).read()


long_description = _read("README.md")

requirements = [
    "compas_fab ~= 0.11",
    "compas_rrc ~= 1.0.0",
    "questionary ~= 1.5.1",
    "confuse ~= 1.3.0",
    "docker ~= 4.2.2",
    "couchdb == 1.2",
]

extras_require = {
    "dev": [
        "attrs ~= 19.3",
        "black ~= 19.10b0",
        "doc8",
        "flake8",
        "invoke >= 0.14",
        "isort",
        "pydocstyle",
        "pytest >= 3.2",
        "recommonmark >=0.6",
        "sphinx_compas_theme >= 0.4",
        "sphinx >=1.6",
        "setuptools_scm[toml]",
    ]
}

setup(
    name="rapid_clay_formations_fab",
    description="Fabrication code for Rapid Clay Formations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gramaziokohler.github.io/rapid_clay_formations_fab",
    author="Gramazio Kohler Research",
    maintainer="Anton Tetov",
    maintainer_email="anton@tetov.se",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: IronPython",
    ],
    keywords=["architecture", "engineering", "fabrication", "construction"],
    project_urls={
        "Repository": "https://github.com/gramaziokohler/rapid_clay_formations_fab",
        "Issues": "https://github.com/gramaziokohler/rapid_clay_formations_fab/issues",
        "Documentation": "https://gramaziokohler.github.io/rapid_clay_formations_fab",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    extras_require=extras_require,
    python_requires=">=3.7",  # usage in IronPython is supported, see note in README
    obsoletes=["compas_rcf"],
    entry_points={
        "console_scripts": ["rcf_run = rapid_clay_formations_fab.abb.run:main"]
    },
)
