# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# If your documentation needs a minimal Sphinx version, state it here.
import sphinx_compas_theme

#
# needs_sphinx = "1.0"
from rapid_clay_formations_fab import __version__

# -- General configuration ------------------------------------------------

project = "Rapid Clay Formations Fabrication"
copyright = "MAS DFAB 1920 students and tutors"
author = "Anton T Johansson"
version = release = __version__

master_doc = "index"

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
templates_path = [
    "_templates",
]
exclude_patterns: list = []

pygments_style = "sphinx"
show_authors = True
add_module_names = True
language = None

# -- Extension configuration ------------------------------------------------

extensions = [
    "recommonmark",
    "autoapi.extension",
    "sphinx.ext.autodoc",
    # "sphinx.ext.autosummary",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
]

autoapi_dirs = ["../src"]

autoapi_options = [
    "members",
    "undoc-members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",
]

autodoc_typehints = "description"

# napoleon options

napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = False
napoleon_use_rtype = False


# intersphinx options

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", "https://docs.python.org/3/objects.inv"),
    "compas": (
        "https://compas.dev/compas/latest/",
        "https://compas.dev/compas/latest/objects.inv",
    ),
    "compas_fab": (
        "https://gramaziokohler.github.io/compas_fab/latest/",
        "https://gramaziokohler.github.io/compas_fab/latest/objects.inv",
    ),
    "confuse": (
        "https://confuse.readthedocs.io/en/latest/",
        "https://confuse.readthedocs.io/en/latest/objects.inv",
    ),
}

# -- Options for HTML output ----------------------------------------------

html_theme = "compaspkg"
html_theme_path = sphinx_compas_theme.get_html_theme_path()

html_theme_options = {
    "package_name": "rapid_clay_formations_fab",
    "package_title": project,
    "package_version": release,
    "package_repo": "https://github.com/gramaziokohler/rapid_clay_formations_fab",
}

html_context: dict = {}
html_static_path: list = []
html_extra_path = [".nojekyll"]
html_last_updated_fmt = ""
html_copy_source = False
html_show_sourcelink = True
html_add_permalinks = ""
html_experimental_html5_writer = True
html_compact_lists = True
