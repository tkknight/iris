# Copyright Iris contributors
#
# This file is part of Iris and is released under the LGPL license.
# See COPYING and COPYING.LESSER in the root of the repository for full
# licensing details.

# -*- coding: utf-8 -*-
#
# Iris documentation build configuration file, created by
# sphinx-quickstart on Tue May 25 13:26:23 2010.
#
# This file is execfile()d with the current directory set to its containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# ----------------------------------------------------------------------------

import datetime
import ntpath
import os
from pathlib import Path
import re
import sys
import warnings

import iris


# function to write  useful output to stdout, prefixing the source.
def autolog(message):
    print("[{}] {}".format(ntpath.basename(__file__), message))


# -- Check for dev make options to build quicker
skip_api = os.environ.get("SKIP_API")

# -- Are we running on the readthedocs server, if so do some setup -----------
on_rtd = os.environ.get("READTHEDOCS") == "True"

if on_rtd:
    autolog("Build running on READTHEDOCS server")

    # list all the READTHEDOCS environment variables that may be of use
    # at some point
    autolog("Listing all environment variables on the READTHEDOCS server...")

    for item, value in os.environ.items():
        autolog("[READTHEDOCS] {} = {}".format(item, value))

# This is the rtd reference to the version, such as: latest, stable, v3.0.1 etc
# For local testing purposes this could be explicitly set latest or stable.
rtd_version = os.environ.get("READTHEDOCS_VERSION")

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# custom sphinx extensions
sys.path.append(os.path.abspath("sphinxext"))

# add some sample files from the developers guide..
sys.path.append(os.path.abspath(os.path.join("developers_guide")))

# why isnt the iris path added to it is discoverable too?  We dont need to,
# the sphinext to generate the api rst knows where the source is.  If it
# is added then the travis build will likely fail.

# -- Project information -----------------------------------------------------

project = "Iris"

# define the copyright information for latex builds. Note, for html builds,
# the copyright exists directly inside "_templates/layout.html"
copyright_years = f"2010 - {datetime.datetime.now().year}"
copyright = f"{copyright_years}, Iris Contributors"
author = "Iris Developers"

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

# The short X.Y version.
if iris.__version__ == "dev":
    version = "dev"
else:
    # major.minor.patch-dev -> major.minor.patch
    version = ".".join(iris.__version__.split("-")[0].split(".")[:3])
# The full version, including alpha/beta/rc tags.
release = iris.__version__

autolog("Iris Version = {}".format(version))
autolog("Iris Release = {}".format(release))

# -- General configuration ---------------------------------------------------

# Create a variable that can be inserted in the rst "|copyright_years|".
# You can add more variables here if needed.

build_python_version = ".".join([str(i) for i in sys.version_info[:3]])


def _dotv(version):
    result = version
    match = re.match(r"^py(\d+)$", version)
    if match:
        digits = match.group(1)
        if len(digits) > 1:
            result = f"{digits[0]}.{digits[1:]}"
    return result


# Automate the discovery of the python versions tested with CI.
python_support = sorted(
    [fname.stem for fname in Path(".").glob("../../requirements/ci/py*.yml")]
)

if not python_support:
    python_support = "unknown Python versions"
elif len(python_support) == 1:
    python_support = f"Python {_dotv(python_support[0])}"
else:
    rest = ", ".join([_dotv(v) for v in python_support[:-1]])
    last = _dotv(python_support[-1])
    python_support = f"Python {rest} and {last}"

rst_epilog = f"""
.. |copyright_years| replace:: {copyright_years}
.. |python_version| replace:: {build_python_version}
.. |python_support| replace:: {python_support}
.. |iris_version| replace:: v{version}
.. |build_date| replace:: ({datetime.datetime.now().strftime('%d %b %Y')})
"""

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.duration",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.extlinks",
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinx.ext.napoleon",
    "sphinx_panels",
    # TODO: Spelling extension disabled until the dependencies can be included
    # "sphinxcontrib.spelling",
    "sphinx_gallery.gen_gallery",
    "matplotlib.sphinxext.mathmpl",
    "matplotlib.sphinxext.plot_directive",
]

if skip_api == "1":
    autolog("Skipping the API docs generation (SKIP_API=1)")
else:
    # better api documentation (custom)
    extensions.extend(
        ["custom_class_autodoc", "custom_data_autodoc", "generate_package_rst"]
    )

# -- panels extension ---------------------------------------------------------
# See https://sphinx-panels.readthedocs.io/en/latest/

# -- Napoleon extension -------------------------------------------------------
# See https://sphinxcontrib-napoleon.readthedocs.io/en/latest/sphinxcontrib.napoleon.html
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True  # includes dunders in api doc
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_custom_sections = None

# -- spellingextension --------------------------------------------------------
# See https://sphinxcontrib-spelling.readthedocs.io/en/latest/customize.html
spelling_lang = "en_GB"
# The lines in this file must only use line feeds (no carriage returns).
spelling_word_list_filename = ["spelling_allow.txt"]
spelling_show_suggestions = False
spelling_show_whole_line = False
spelling_ignore_importable_modules = True
spelling_ignore_python_builtins = True

# -- copybutton extension -----------------------------------------------------
# See https://sphinx-copybutton.readthedocs.io/en/latest/
copybutton_prompt_text = ">>> "

# sphinx.ext.todo configuration -----------------------------------------------
# See https://www.sphinx-doc.org/en/master/usage/extensions/todo.html
todo_include_todos = True

# api generation configuration
autodoc_member_order = "groupwise"
autodoc_default_flags = ["show-inheritance"]
autosummary_generate = True
autosummary_imported_members = True
autopackage_name = ["iris"]
autoclass_content = "init"
modindex_common_prefix = ["iris"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# -- intersphinx extension ----------------------------------------------------
# See https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html
intersphinx_mapping = {
    "cartopy": ("https://scitools.org.uk/cartopy/docs/latest/", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
    "numpy": ("https://numpy.org/doc/stable/", None),
    "python": ("https://docs.python.org/3/", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/", None),
}

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# -- plot_directive extension -------------------------------------------------
# See https://matplotlib.org/stable/api/sphinxext_plot_directive_api.html#options
plot_formats = [
    ("png", 100),
]

# -- Extlinks extension -------------------------------------------------------
# See https://www.sphinx-doc.org/en/master/usage/extensions/extlinks.html

extlinks = {
    "issue": ("https://github.com/SciTools/iris/issues/%s", "Issue #"),
    "pull": ("https://github.com/SciTools/iris/pull/%s", "PR #"),
    "issue_only": ("https://github.com/SciTools/iris/issues/%s", ""),
    "author": ("https://github.com/%s", "@"),
}

# -- Doctest ("make doctest")--------------------------------------------------

doctest_global_setup = "import iris"

# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_logo = "_static/iris-logo-title.png"
html_favicon = "_static/favicon.ico"
html_theme = "sphinx_rtd_theme"

html_theme_options = {
    "display_version": True,
    "style_external_links": True,
    "logo_only": "True",
}

html_context = {
    "rtd_version": rtd_version,
    "version": version,
    "copyright_years": copyright_years,
    "python_version": build_python_version,
    # menu_links and menu_links_name are used in _templates/layout.html
    # to include some nice icons.  See http://fontawesome.io for a list of
    # icons (used in the sphinx_rtd_theme)
    "menu_links_name": "Support",
    "menu_links": [
        (
            '<i class="fa fa-github fa-fw"></i> Source Code',
            "https://github.com/SciTools/iris",
        ),
        (
            '<i class="fa fa-comments fa-fw"></i> GitHub Discussions',
            "https://github.com/SciTools/iris/discussions",
        ),
        (
            '<i class="fa fa-question fa-fw"></i> StackOverflow for "How Do I?"',
            "https://stackoverflow.com/questions/tagged/python-iris",
        ),
        (
            '<i class="fa fa-book fa-fw"></i> Legacy Documentation',
            "https://scitools.org.uk/iris/docs/v2.4.0/index.html",
        ),
    ],
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
html_style = "theme_override.css"

# this allows for using datatables: https://datatables.net/
html_css_files = [
    "https://cdn.datatables.net/1.10.23/css/jquery.dataTables.min.css",
]

html_js_files = [
    "https://cdn.datatables.net/1.10.23/js/jquery.dataTables.min.js",
]

# url link checker.  Some links work but report as broken, lets ignore them.
# See https://www.sphinx-doc.org/en/1.2/config.html#options-for-the-linkcheck-builder
linkcheck_ignore = [
    "http://cfconventions.org",
    "http://code.google.com/p/msysgit/downloads/list",
    "http://effbot.org",
    "https://github.com",
    "http://www.personal.psu.edu/cab38/ColorBrewer/ColorBrewer_updates.html",
    "http://schacon.github.com/git",
    "http://scitools.github.com/cartopy",
    "http://www.wmo.int/pages/prog/www/DPFS/documents/485_Vol_I_en_colour.pdf",
    "https://software.ac.uk/how-cite-software",
    "http://www.esrl.noaa.gov/psd/data/gridded/conventions/cdc_netcdf_standard.shtml",
    "http://www.nationalarchives.gov.uk/doc/open-government-licence",
]

# list of sources to exclude from the build.
exclude_patterns = []

# -- sphinx-gallery config ----------------------------------------------------
# See https://sphinx-gallery.github.io/stable/configuration.html

sphinx_gallery_conf = {
    # path to your example scripts
    "examples_dirs": ["../gallery_code"],
    # path to where to save gallery generated output
    "gallery_dirs": ["generated/gallery"],
    # filename pattern for the files in the gallery
    "filename_pattern": "/plot_",
    # filename patternt to ignore in the gallery
    "ignore_pattern": r"__init__\.py",
}

# -----------------------------------------------------------------------------
# Remove matplotlib agg warnings from generated doc when using plt.show
warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    message="Matplotlib is currently using agg, which is a"
    " non-GUI backend, so cannot show the figure.",
)

# -- numfig options (built-in) ------------------------------------------------
# Enable numfig.
numfig = True

numfig_format = {
    "code-block": "Example %s",
    "figure": "Figure %s",
    "section": "Section %s",
    "table": "Table %s",
}
