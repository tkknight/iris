.. _iris_docs:

Iris |version|
========================

**A powerful, format-agnostic, community-driven Python package for analysing
and visualising Earth science data.**

Iris implements a data model based on the `CF conventions <http://cfconventions.org>`_
giving you a powerful, format-agnostic interface for working with your data.
It excels when working with multi-dimensional Earth Science data, where tabular
representations become unwieldy and inefficient.

`CF Standard names <http://cfconventions.org/standard-names.html>`_,
`units <https://github.com/SciTools/cf_units>`_, and coordinate metadata
are built into Iris, giving you a rich and expressive interface for maintaining
an accurate representation of your data. Its treatment of data and
associated metadata as first-class objects includes:

* visualisation interface based on `matplotlib <https://matplotlib.org/>`_ and
  `cartopy <https://scitools.org.uk/cartopy/docs/latest/>`_,
* unit conversion,
* subsetting and extraction,
* merge and concatenate,
* aggregations and reductions (including min, max, mean and weighted averages),
* interpolation and regridding (including nearest-neighbor, linear and
  area-weighted), and
* operator overloads (``+``, ``-``, ``*``, ``/``, etc.).

A number of file formats are recognised by Iris, including CF-compliant NetCDF,
GRIB, and PP, and it has a plugin architecture to allow other formats to be
added seamlessly.

Building upon `NumPy <http://www.numpy.org/>`_ and
`dask <https://dask.pydata.org/en/latest/>`_, Iris scales from efficient
single-machine workflows right through to multi-core clusters and HPC.
Interoperability with packages from the wider scientific Python ecosystem comes
from Iris' use of standard NumPy/dask arrays as its underlying data storage.

Iris is part of SciTools, for more information see https://scitools.org.uk/.
For **Iris 2.4** and earlier documentation please see the
:link-badge:`https://scitools.org.uk/iris/docs/v2.4.0/,"legacy documentation",cls=badge-info text-white`.


.. panels::
    :card: + intro-card text-center
    :column: col-lg-6 col-md-6 col-sm-6 col-xs-12 d-flex

    ---
    :img-top: _static/index_getting_started.svg

    Getting started
    ^^^^^^^^^^^^^^^

    New to *pandas*? Check out the getting started guides. They contain an
    introduction to *pandas'* main concepts and links to additional tutorials.

    +++

    .. link-button:: getting_started
                   :type: ref
            :text: To the getting started guides
            :classes: btn-block btn-secondary stretched-link


.. panels::
    :container: container-lg pb-3
    :column: col-lg-4 col-md-4 col-sm-6 col-xs-12 p-2

    Install Iris as a user or developer.
    +++
    .. link-button:: installing_iris
        :type: ref
        :text: Installing Iris
        :classes: btn-outline-primary btn-block
    ---
    Example code to create a variety of plots.
    +++
    .. link-button:: sphx_glr_generated_gallery
        :type: ref
        :text: Gallery
        :classes: btn-outline-primary btn-block
    ---
    Find out what has recently changed in Iris.
    +++
    .. link-button:: iris_whatsnew
        :type: ref
        :text: What's New
        :classes: btn-outline-primary btn-block
    ---
    Learn how to use Iris.
    +++
    .. link-button:: user_guide_index
        :type: ref
        :text: User Guide
        :classes: btn-outline-primary btn-block
    ---
    Browse full Iris functionality by module.
    +++
    .. link-button:: Iris
        :type: ref
        :text: Iris API
        :classes: btn-outline-primary btn-block
    ---
    As a developer you can contribute to Iris.
    +++
    .. link-button:: development_where_to_start
        :type: ref
        :text: Getting Involved
        :classes: btn-outline-primary btn-block


.. toctree::
   :maxdepth: 1
   :caption: Getting Started
   :hidden:

   installing
   generated/gallery/index


.. toctree::
   :maxdepth: 1
   :caption: User Guide
   :name: userguide_index
   :hidden:

   userguide/index



.. _developers_guide:

.. toctree::
   :maxdepth: 1
   :caption: Further Topics
   :hidden:

   further_topics/index


.. toctree::
   :maxdepth: 1
   :caption: Developers Guide
   :name: development_index
   :hidden:

   developers_guide/contributing_getting_involved


.. toctree::
   :maxdepth: 1
   :caption: Reference
   :hidden:

   generated/api/iris

