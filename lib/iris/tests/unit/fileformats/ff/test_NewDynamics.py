# Copyright Iris contributors
#
# This file is part of Iris and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Unit tests for :class:`iris.fileformat.ff.NewDynamics`."""

import numpy as np

from iris.fileformats._ff import NewDynamics
from iris.tests import _shared_utils


class TestNewDynamics:
    """Test ewDynamics."""
    def test_class_attributes(self):  # noqa: D102
        reals = np.arange(6) + 100
        grid = NewDynamics(None, None, reals, None)
        assert grid._v_offset == 0.5


class Test__y_vectors:
    """Test  y vectors."""
    def _test(self, row, yp, yv):
        reals = np.arange(6) + 100
        grid = NewDynamics(None, row, reals, None)
        result_yp, result_yv = grid._y_vectors()
        _shared_utils.assert_array_equal(result_yp, yp)
        _shared_utils.assert_array_equal(result_yv, yv)

    def test_none(self):  # noqa: D102
        self._test(row=None, yp=None, yv=None)

    def test_1d(self):  # noqa: D102
        self._test(
            row=np.array([[0], [1], [2], [3]]),
            yp=np.array([0, 1, 2, 3]),
            yv=None,
        )

    def test_2d(self):  # noqa: D102
        self._test(
            row=np.array([[0, 0], [1, 10], [2, 20], [3, 30]]),
            yp=np.array([0, 1, 2, 3]),
            yv=np.array([0, 10, 20]),
        )
