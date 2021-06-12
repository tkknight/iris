.. _iris_docs:

Iris |version|
========================

**A powerful, format-agnostic, community-driven Python package for analysing
and visualising Earth science data.**

Iris implements a data model based on the `CF conventions <http://cfconventions.org>`_
giving you a powerful, format-agnostic interface for working with your data.
It excels when working with multi-dimensional Earth Science data, where tabular
representations become unwieldy and inefficient.

For more information see :ref:`why_iris`.

Iris is part of SciTools, for more information see https://scitools.org.uk/.
For **Iris 2.4** and earlier documentation please see the
:link-badge:`https://scitools.org.uk/iris/docs/v2.4.0/,"legacy documentation",cls=badge-info text-white`.

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

   why_iris
   installing
   generated/gallery/index


.. toctree::
   :maxdepth: 1
   :caption: User Guide
   :name: userguide_index
   :hidden:

   userguide/index
   userguide/iris_cubes
   userguide/loading_iris_cubes
   userguide/saving_iris_cubes
   userguide/navigating_a_cube
   userguide/subsetting_a_cube
   userguide/real_and_lazy_data
   userguide/plotting_a_cube
   userguide/interpolation_and_regridding
   userguide/merge_and_concat
   userguide/cube_statistics
   userguide/cube_maths
   userguide/citation
   userguide/code_maintenance


.. _developers_guide:

.. toctree::
   :maxdepth: 1
   :caption: Further Topics
   :hidden:

   further_topics/index
   further_topics/metadata
   further_topics/lenient_metadata
   further_topics/lenient_maths


.. toctree::
   :maxdepth: 1
   :caption: Developers Guide
   :name: development_index
   :hidden:

   developers_guide/contributing_getting_involved
   developers_guide/gitwash/index
   developers_guide/contributing_documentation
   developers_guide/contributing_codebase_index
   developers_guide/contributing_changes
   developers_guide/release


.. toctree::
   :maxdepth: 1
   :caption: Reference
   :hidden:

   generated/api/iris
   whatsnew/index
   techpapers/index
   copyright
