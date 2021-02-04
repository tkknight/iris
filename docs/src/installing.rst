.. _installing_iris:

Installing Iris
===============

Iris is available using conda for the following platforms:

* Linux 64-bit,
* Mac OSX 64-bit, and
* Windows 64-bit.

Windows 10 now has support for Linux distributions via WSL_ (Windows
Subsystem for Linux).  This is a great option to get started with Iris
for users and developers.  Be aware that we do not currently test against
any WSL_ distributions.

.. _WSL: https://docs.microsoft.com/en-us/windows/wsl/install-win10

.. note:: Iris currently supports and is tested against **Python 3.6** and
          **Python 3.7**.


.. _installing_using_conda:

Installing Using Conda (Users)
------------------------------

To install Iris using conda, you must first download and install conda,
for example from https://docs.conda.io/en/latest/miniconda.html.

Once conda is installed, you can install Iris using conda with the following
command::

  conda install -c conda-forge iris

If you wish to run any of the code in the gallery you will also
need the Iris sample data. This can also be installed using conda::

  conda install -c conda-forge iris-sample-data

Further documentation on using conda and the features it provides can be found
at https://conda.io/en/latest/index.html.

.. _installing_from_source_without_conda:

Installing from Source Without Conda on Debian-Based Linux Distros (Developers)
-------------------------------------------------------------------------------

Iris can also be installed without a conda environment. The instructions in
this section are valid for Debian-based Linux distributions (Debian, Ubuntu,
Kubuntu, etc.).

Iris and its dependencies need some shared libraries in order to work properly.
These can be installed
with apt::

  sudo apt-get install python3-pip python3-tk libudunits2-dev libproj-dev proj-bin libgeos-dev libcunit1-dev

Consider executing::

  sudo apt-get update

before and after installation of Debian packages.

The rest can be done with pip. Begin with numpy::

  pip3 install numpy

Finally, Iris and its Python dependencies can be installed with the following
command::

  pip3 install setuptools cftime==1.2.1 cf-units scitools-pyke scitools-iris

This procedure was tested on a Ubuntu 20.04 system on the
27th of January, 2021.
Be aware that through updates of the involved Debian and/or Python packages,
dependency conflicts might arise or the procedure might have to modified.

.. _installing_from_source:

Installing from Source with Conda (Developers)
----------------------------------------------

The latest Iris source release is available from
https://github.com/SciTools/iris.

For instructions on how to obtain the Iris project source from GitHub see
:ref:`forking` and :ref:`set-up-fork` for instructions.

Once conda is installed, you can install Iris using conda and then activate
it.  The example commands below assume you are in the root directory of your
local copy of Iris::

  conda env create --file=requirements/ci/iris.yml
  conda activate iris-dev

The ``requirements/ci/iris.yml`` file defines the Iris development conda
environment *name* and all the relevant *top level* `conda-forge` package
dependencies that you need to **code**, **test**, and **build** the
documentation.  If you wish to minimise the environment footprint, simply
remove any unwanted packages from the requirements file e.g., if you don't
intend to run the Iris tests locally or build the documentation, then remove
all the packages from the `testing` and `documentation` sections.

.. note:: The ``requirements/ci/iris.yml`` file will always use the latest
          Iris tested Python version available.  For all Python versions that
          are supported and tested against by Iris, view the contents of
          the `requirements/ci`_ directory.

.. _requirements/ci: https://github.com/scitools/iris/tree/master/requirements/ci

Finally you need to run the command to configure your shell environment
to find your local Iris code::

  python setup.py develop


Running the Tests
-----------------

To ensure your setup is configured correctly you can run the test suite using
the command::

    python setup.py test

For more information see :ref:`developer_running_tests`.


Custom Site Configuration
-------------------------

The default site configuration values can be overridden by creating the file
``iris/etc/site.cfg``. For example, the following snippet can be used to
specify a non-standard location for your dot executable::

  [System]
  dot_path = /usr/bin/dot

An example configuration file is available in ``iris/etc/site.cfg.template``.
See :py:func:`iris.config` for further configuration options.
