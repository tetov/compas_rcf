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
    "rapid_clay_formations_fab",
]

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
        "Development Status :: 7 - Inactive",
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
    python_requires=">=3.7",  # usage in IronPython is supported, see note in README
)
