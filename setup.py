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
    "compas_fab ~= 0.10.2",
    "compas_rrc ~= 0.2.2",
    "questionary ~= 1.5.1",
    "confuse ~= 1.0.0",
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
        "sphinx > =1.6",
        "setuptools_scm[toml]",
    ]
}

setup(
    name="compas_rcf",
    description="python module for MAS DFAB project Rapid Clay Formations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tetov/compas_rcf",
    author="Anton T Johansson",
    author_email="anton@tetov.se",
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
        "Repository": "https://github.com/compas-dev/compas",
        "Issues": "https://github.com/compas-dev/compas/issues",
        "Documentation": "https://compas_rcf.tetov.se/",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    install_requires=requirements,
    extras_require=extras_require,
    python_requires=">=3.7",  # usage in IronPython is supported, see note in README
    entry_points={"console_scripts": []},
)
