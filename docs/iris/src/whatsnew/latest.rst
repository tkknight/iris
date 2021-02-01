.. include:: ../common_links.inc

<unreleased>
************

This document explains the changes made to Iris for this release
(:doc:`View all changes <index>`.)


.. dropdown:: :opticon:`report` Release Highlights
   :container: + shadow
   :title: text-primary text-center font-weight-bold
   :body: bg-light
   :animate: fade-in
   :open:

   The highlights for this major/minor release of Iris include:

   * N/A

   And finally, get in touch with us on `GitHub`_ if you have any issues or
   feature requests for improving Iris. Enjoy!


📢 Announcements
================

#. N/A


✨ Features
===========

#. `@pelson`_ and `@trexfeathers`_ enhanced :meth:iris.plot.plot and
   :meth:iris.quickplot.plot to automatically place the cube on the x axis if
   the primary coordinate being plotted against is a vertical coordinate. E.g.
   ``iris.plot.plot(z_cube)`` will produce a z-vs-phenomenon plot, where before
   it would have produced a phenomenon-vs-z plot. (:pull:`3906`)


🐛 Bugs Fixed
=============

#. `@gcaria`_ fixed :meth:`~iris.cube.Cube.cell_measure_dims` to also accept the
   string name of a :class:`~iris.coords.CellMeasure`. (:pull:`3931`)

#. `@gcaria`_ fixed :meth:`~iris.cube.Cube.ancillary_variable_dims` to also accept
   the string name of a :class:`~iris.coords.AncillaryVariable`. (:pull:`3931`)


💣 Incompatible Changes
=======================

#. N/A


🔥 Deprecations
===============

#. N/A


🔗 Dependencies
===============

#. N/A


📚 Documentation
================

#. `@rcomer`_ updated the "Seasonal ensemble model plots" Gallery example. (:pull:`3933`)

#. `@MHBalsmeier`_ described non-conda installation on Debian-based distros. (:pull:`3958`)

#. `@bjlittle`_ clarified in the doc-string that :class:`~iris.coords.Coord` is now an `abstract base class`_ of
   coordinates since ``v3.0.0``, and it is **not** possible to create an instance of it. (:pull:`3971`)


💼 Internal
===========

#. `@rcomer`_ removed an old unused test file. (:pull:`3913`)


.. comment
    Whatsnew author names (@github name) in alphabetical order. Note that,
    core dev names are automatically included by the common_links.inc:

.. _@gcaria: https://github.com/gcaria
.. _@MHBalsmeier: https://github.com/MHBalsmeier


.. comment
    Whatsnew resources in alphabetical order:

.. _abstract base class: https://docs.python.org/3/library/abc.html
.. _GitHub: https://github.com/SciTools/iris/issues/new/choose
