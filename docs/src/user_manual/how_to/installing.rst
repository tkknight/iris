.. how-to:: Installing
   :tags: topic_about

   How to install the Iris Python package.

.. _installing_iris:

Installing
==========

.. readingtime::

Iris can be installed using conda or pip.

.. note:: Iris is currently supported and tested against |python_support|
          running on Linux.  We do not currently actively test on other
          platforms such as Windows or macOS.

          Windows 10 now has support for Linux distributions via WSL_ (Windows
          Subsystem for Linux).  This is a great option to get started with
          Iris for users and contributors.  Be aware that we do not currently
          test against any WSL_ distributions.

.. _WSL: https://learn.microsoft.com/en-us/windows/wsl/install

.. note:: This documentation was built using Python |python_version|.


.. _installing_a_released_version:

Installing a Released Version
-----------------------------

.. tab-set::

    .. tab-item:: conda-forge

        To install Iris using conda, you must first download and install conda,
        for example from https://docs.conda.io/en/latest/miniconda.html.

        Once conda is installed, you can install Iris using conda with the following
        command::

          conda install -c conda-forge iris

        If you wish to run any of the code in the gallery you will also
        need the Iris sample data. This can also be installed using conda::

          conda install -c conda-forge iris-sample-data

        Further documentation on using conda and the features it provides can be found
        at https://docs.conda.io/projects/conda/en/latest/index.html.

    .. tab-item:: PyPI

        Iris is also available from https://pypi.org/ so can be installed with ``pip``::

          pip install scitools-iris

        If you wish to run any of the code in the gallery you will also
        need the Iris sample data. This can also be installed using pip::

          pip install iris-sample-data



.. _installing_from_source:

Installing a Development Version
--------------------------------

The latest Iris source release is available from
https://github.com/SciTools/iris.

For instructions on how to obtain the Iris project source from GitHub see
:ref:`forking` and :ref:`set-up-fork` for instructions.

Install `Pixi <https://pixi.sh/>`_ and create the Iris development environment
from the repository root::

  pixi install --environment dev-py314

The Pixi environments in ``pyproject.toml`` define Conda and PyPI packages for
development, testing, documentation, and optional integrations. Select a
different environment to use another supported Python version or package set.
The development environment installs the local Iris checkout in editable mode.


Running the Tests
-----------------

To ensure your setup is configured correctly you can run the test suite using
the command::

    pytest

For more information see :ref:`test manual env`.


Custom Site Configuration
-------------------------

The default site configuration values can be overridden by creating the file
``iris/etc/site.cfg``. For example, the following snippet can be used to
specify a non-standard location for your dot executable::

  [System]
  dot_path = /usr/bin/dot

An example configuration file is available in ``iris/etc/site.cfg.template``.
See :py:func:`iris.config` for further configuration options.
