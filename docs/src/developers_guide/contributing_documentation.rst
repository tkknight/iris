
.. _contributing.documentation:

Contributing to the Documentation
---------------------------------

Documentation is important and we encourage any improvements that can be made.
If you believe the documentation is not clear please contribute a change to
improve the documentation for all users.

Any change to the Iris project whether it is a bugfix, new feature or
documentation update must use the :ref:`development-workflow`.


Requirements
~~~~~~~~~~~~

The documentation uses specific packages that need to be present.  Please see
:ref:`installing_iris` for instructions.


.. _contributing.documentation.building:

Building
~~~~~~~~

This documentation was built using the latest Python version that Iris
supports.  For more information see :ref:`installing_iris`.

The build can be run from the documentation directory ``docs/src``.

The build output for the html is found in the ``_build/html`` sub directory.
When updating the documentation ensure the html build has *no errors* or
*warnings* otherwise it may fail the automated `cirrus-ci`_  build.

Once the build is complete, if it is rerun it will only rebuild the impacted
build artefacts so should take less time.

There is also an option to perform a build but skip the
:ref:`contributing.documentation.gallery` creation completely.  This can be
achieved via::

    make html-noplot

If you wish to run a clean build you can run::

    make clean
    make html

This is useful for a final test before committing your changes.

.. note:: In order to preserve a clean build for the html, all **warnings**
          have been promoted to be **errors** to ensure they are addressed.
          This **only** applies when ``make html`` is run.

.. _cirrus-ci: https://cirrus-ci.com/github/SciTools/iris

.. _contributing.documentation.testing:

Testing
~~~~~~~

There are a ways to test various aspects of the documentation.  The
``make`` commands shown below can be run in the ``docs`` or
``docs/src`` directory.

Each :ref:`contributing.documentation.gallery` entry has a corresponding test.
To run the tests::

    make gallerytest

Many documentation pages includes python code itself that can be run to ensure
it is still valid or to demonstrate examples.  To ensure these tests pass
run::

    make doctest

See :data:`iris.cube.Cube.data` for an example of using the `doctest`_
approach.

.. _doctest: http://www.sphinx-doc.org/en/stable/ext/doctest.html

The hyperlinks in the documentation can be checked automatically.
If there is a link that is known to work it can be excluded from the checks by
adding it to the ``linkcheck_ignore`` array that is defined in the
`conf.py`_.  The hyperlink check can be run via::

    make linkcheck

If this fails check the output for the text **broken** and then correct
or ignore the url.

.. comment
    Finally, the spelling in the documentation can be checked automatically via the
    command::

        make spelling

    The spelling check may pull up many technical abbreviations and acronyms.  This
    can be managed by using an **allow** list in the form of a file.  This file,
    or list of files is set in the `conf.py`_ using the string list
    ``spelling_word_list_filename``.


.. note:: In addition to the automated `cirrus-ci`_ build of all the
          documentation build options above, the
          https://readthedocs.org/ service is also used.  The configuration
          of this held in a file in the root of the
          `github Iris project <https://github.com/SciTools/iris>`_  named
          ``.readthedocs.yml``.


.. _conf.py: https://github.com/SciTools/iris/blob/main/docs/src/conf.py


.. _contributing.documentation.api:

Generating API Documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to auto generate the API documentation based upon the docstrings a
custom set of python scripts are used, these are located in the directory
``docs/src/sphinxext``.  Once the ``make html`` command has been run,
the output of these scripts can be found in
``docs/src/generated/api``.

If there is a particularly troublesome module that breaks the ``make html`` you
can exclude the module from the API documentation.  Add the entry to the
``exclude_modules`` tuple list in the
``docs/src/sphinxext/generate_package_rst.py`` file.


.. _contributing.documentation.gallery:

Gallery
~~~~~~~

The Iris :ref:`sphx_glr_generated_gallery` uses a sphinx extension named
`sphinx-gallery <https://sphinx-gallery.github.io/stable/>`_
that auto generates reStructuredText (rst) files based upon a gallery source
directory that abides directory and filename convention.

The code for the gallery entries are in ``docs/gallery_code``.
Each sub directory in this directory is a sub section of the gallery.  The
respective ``README.rst`` in each folder is included in the gallery output.

For each gallery entry there must be a corresponding test script located in
``docs/gallery_tests``.

To add an entry to the gallery simple place your python code into the
appropriate sub directory and name it with a prefix of ``plot_``.  If your
gallery entry does not fit into any existing sub directories then create a new
directory and place it in there.

The reStructuredText (rst) output of the gallery is located in
``docs/src/generated/gallery``.

For more information on the directory structure and options please see the
`sphinx-gallery getting started
<https://sphinx-gallery.github.io/stable/getting_started.html>`_ documentation.
