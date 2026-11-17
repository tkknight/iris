# Copyright Iris contributors
#
# This file is part of Iris and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Unit tests for the `iris.plot.pcolor` function."""

from iris.tests import _shared_utils
from iris.tests.unit.plot import TestGraphicStringCoord
from iris.tests.unit.plot._blockplot_common import (
    Mixin2dCoordsContigTol,
    Mixin2dCoordsPlot,
    MixinStringCoordPlot,
)

if _shared_utils.MPL_AVAILABLE:
    import iris.plot as iplt

    PLOT_FUNCTION_TO_TEST = iplt.pcolor


@_shared_utils.skip_plot
class TestStringCoordPlot(MixinStringCoordPlot, TestGraphicStringCoord):
    """Test tringCoordPlot."""
    def blockplot_func(self):  # noqa: D102
        return PLOT_FUNCTION_TO_TEST


@_shared_utils.skip_plot
class Test2dCoords(Mixin2dCoordsPlot):
    """Test dCoords."""
    def blockplot_func(self):  # noqa: D102
        return PLOT_FUNCTION_TO_TEST


@_shared_utils.skip_plot
class Test2dContigTol(Mixin2dCoordsContigTol):
    """Test dContigTol."""
    # Extra call kwargs expected.
    additional_kwargs = dict(antialiased=True, snap=False)

    def blockplot_func(self):  # noqa: D102
        return PLOT_FUNCTION_TO_TEST
