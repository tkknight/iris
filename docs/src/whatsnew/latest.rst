.. include:: ../common_links.inc

|iris_version| |build_date| [unreleased]
****************************************

This document explains the changes made to Iris for this release
(:doc:`View all changes <index>`.)

.. admonition:: |iris_version| Release Highlights

   The highlights for this major/minor release of Iris include:

   * N/A

   And finally, get in touch with us on :issue:`GitHub<new/choose>` if you have
   any issues or feature requests for improving Iris. Enjoy!


📢 Announcements
================

#. Congratulations to `@ESadek-MO`_ who has become a core developer for Iris! 🎉


✨ Features
===========

#. N/A


🐛 Bugs Fixed
=============

#. N/A


💣 Incompatible Changes
=======================

#. N/A


🚀 Performance Enhancements
===========================

#. N/A


🔥 Deprecations
===============

#. N/A


🔗 Dependencies
===============

#. N/A


📚 Documentation
================

#. `@rcomer`_ clarified instructions for updating gallery tests. (:pull:`5100`)
#. `@tkknight`_ unpinned ``pydata-sphinx-theme`` and set the default to use
   the light version (not dark) while we make the docs dark mode friendly
   (:pull:`5129`)

#. `@rcomer`_ linked the :obj:`~iris.analysis.PERCENTILE` aggregator from the
   :obj:`~iris.analysis.MEDIAN` docstring, noting that the former handles lazy
   data. (:pull:`5128`)


💼 Internal
===========

#. `@fnattino`_ changed the order of ``ncgen`` arguments in the command to
   create NetCDF files for testing  (caused errors on OS X). (:pull:`5105`)

#. `@rcomer`_ removed some old infrastructure that printed test timings.
   (:pull:`5101`)


.. comment
    Whatsnew author names (@github name) in alphabetical order. Note that,
    core dev names are automatically included by the common_links.inc:

.. _@fnattino: https://github.com/fnattino


.. comment
    Whatsnew resources in alphabetical order:

