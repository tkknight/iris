.. include:: ../common_links.inc

.. _developer_running_tests:

Running the Tests
*****************

.. readingtime::

There are two options for running the tests:

* Use an environment you created yourself.  This requires more manual steps to
  set up, but gives you more flexibility.  For example, you can run a subset of
  the tests or use ``python`` interactively to investigate any issues.  See
  :ref:`test manual env`.

* Use Pixi to create a reproducible environment and run the same tasks as
  continuous integration. See :ref:`using pixi`.

.. _test manual env:

Testing Iris in a Manually Created Environment
==============================================

To create a suitable environment for running the tests, see :ref:`installing_from_source`.

Many Iris tests will use data that may be defined in the test itself, however
this is not always the case as sometimes example files may be used.  Due to
the size of some of the files used these are not kept in the Iris repository.
A separate repository under the `SciTools`_ organisation is used, see
https://github.com/SciTools/iris-test-data.

In order to run the tests with **all** the test data you must clone the
``iris-test-data`` repository and then ensure the Iris tests can access
``iris-test-data/test_data``, using one of two methods:

* Store the path in a shell environment variable named **OVERRIDE_TEST_DATA_REPOSITORY**.
* Store the path in ``lib/iris/etc/site.cfg`` (see :mod:`iris.config` for more).

The example command below uses ``~/projects`` as the parent directory::

   cd ~/projects
   git clone git@github.com:SciTools/iris-test-data.git
   export OVERRIDE_TEST_DATA_REPOSITORY=~/projects/iris-test-data/test_data

All the Iris tests may be run from the root ``iris`` project directory using
``pytest``.  For example::

   pytest -n 2

will run the tests across two processes.  For more options, use the command
``pytest -h``.  Below is a trimmed example of the output::

   ============================= test session starts ==============================
   platform linux -- Python 3.10.5, pytest-7.1.2, pluggy-1.0.0
   rootdir: /path/to/git/clone/iris, configfile: pyproject.toml, testpaths: lib/iris
   plugins: xdist-2.5.0, forked-1.4.0
   gw0 I / gw1 I
   gw0 [6361] / gw1 [6361] 

   ........................................................................ [  1%]
   ........................................................................ [  2%]
   ........................................................................ [  3%]
   ...
   .......................ssssssssssssssssss............................... [ 99%]
   ........................                                                 [100%]
   =============================== warnings summary ===============================
   ...
   -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
   =========================== short test summary info ============================
   SKIPPED [1] lib/iris/tests/experimental/test_raster.py:152: Test requires 'gdal'.
   SKIPPED [1] lib/iris/tests/experimental/test_raster.py:155: Test requires 'gdal'.
   ...
   ========= 6340 passed, 21 skipped, 1659 warnings in 193.57s (0:03:13) ==========

There may be some tests that have been **skipped**.  This is due to a Python
decorator being present in the test script that will intentionally skip a test
if a certain condition is not met.  In the example output above there are
**21** skipped tests. At the point in time when this was run this was due to an
experimental dependency not being present.

.. tip::

   The most common reason for tests to be skipped is when the directory for the
   ``iris-test-data`` has not been set which would shows output such as::

      SKIPPED [1] lib/iris/tests/unit/fileformats/test_rules.py:157: Test(s) require external data.
      SKIPPED [1] lib/iris/tests/unit/fileformats/pp/test__interpret_field.py:97: Test(s) require external data.
      SKIPPED [1] lib/iris/tests/unit/util/test_demote_dim_coord_to_aux_coord.py:29: Test(s) require external data.
      
   All Python decorators that skip tests will be defined in
   ``lib/iris/tests/_shared_utils.py`` with a function name with a prefix of
   ``skip_``.

You can also run a specific test module.  The example below runs the tests for
mapping::

   cd lib/iris/tests
   python test_mapping.py

When running the test directly as above you can view the command line options
using the commands ``python test_mapping.py -h`` or
``python test_mapping.py --help``.

.. tip::  A useful command line option to use is ``-d``.  This will display
          matplotlib_ figures as the tests are run.  For example::

             python test_mapping.py -d

.. _using pixi:

Using Pixi for Testing Iris
========================================

Pixi manages Iris' Conda and PyPI development dependencies and runs the tasks
used by Iris GitHub Actions.

From the Iris repository root, list available tasks with::

  pixi task list

Install an environment for a supported Python version with::

  pixi install --environment test-py314

Run the Iris tests and tool tests with::

  pixi run --environment test-py314 tests

Use ``test-py312`` or ``test-py313`` to select another supported Python
version. To run tests with coverage, use ``tests-coverage`` instead. To run
the gallery tests or documentation doctests, use::

  pixi run --environment test-py314 gallery
  pixi run --environment docs-py314 doctest

Pixi installs the selected environment when needed and runs the task inside it.
Additional arguments are passed to the task after ``--``.

.. _v41.5.0: https://setuptools.readthedocs.io/en/latest/history.html#v41-5-0
