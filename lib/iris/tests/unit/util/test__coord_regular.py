# Copyright Iris contributors
#
# This file is part of Iris and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Test elements of :mod:`iris.util` that deal with checking coord regularity.

Specifically, this module tests the following functions:

  * :func:`iris.util.is_regular`,
  * :func:`iris.util.regular_step`, and
  * :func:`iris.util.points_step`.

"""

import numpy as np
import pytest

from iris.coords import AuxCoord, DimCoord
from iris.exceptions import CoordinateMultiDimError, CoordinateNotRegularError
from iris.util import is_regular, points_step, regular_step


class Test_is_regular:
    """Test is regular."""
    def test_coord_with_regular_step(self):  # noqa: D102
        coord = DimCoord(np.arange(5))
        result = is_regular(coord)
        assert result

    def test_coord_with_irregular_step(self):  # noqa: D102
        # Check that a `CoordinateNotRegularError` is captured.
        coord = AuxCoord(np.array([2, 5, 1, 4]))
        result = is_regular(coord)
        assert not result

    def test_scalar_coord(self):  # noqa: D102
        # Check that a `ValueError` is captured.
        coord = DimCoord(5)
        result = is_regular(coord)
        assert not result

    def test_coord_with_string_points(self):  # noqa: D102
        # Check that a `TypeError` is captured.
        coord = AuxCoord(["a", "b", "c"])
        result = is_regular(coord)
        assert not result


class Test_regular_step:
    """Test regular step."""
    def test_basic(self):  # noqa: D102
        dtype = np.float64
        points = np.arange(5, dtype=dtype)
        coord = DimCoord(points)
        expected = np.mean(np.diff(points))
        result = regular_step(coord)
        assert expected == result
        assert result.dtype == dtype

    def test_2d_coord(self):  # noqa: D102
        coord = AuxCoord(np.arange(8).reshape(2, 4))
        exp_emsg = "Expected 1D coord"
        with pytest.raises(CoordinateMultiDimError, match=exp_emsg):
            regular_step(coord)

    def test_scalar_coord(self):  # noqa: D102
        coord = DimCoord(5)
        exp_emsg = "non-scalar coord"
        with pytest.raises(ValueError, match=exp_emsg):
            regular_step(coord)

    def test_coord_with_irregular_step(self):  # noqa: D102
        name = "latitude"
        coord = AuxCoord(np.array([2, 5, 1, 4]), standard_name=name)
        exp_emsg = "{} is not regular".format(name)
        with pytest.raises(CoordinateNotRegularError, match=exp_emsg):
            regular_step(coord)


class Test_points_step:
    """Test points step."""
    def test_regular_points(self):  # noqa: D102
        regular_points = np.arange(5)
        exp_avdiff = np.mean(np.diff(regular_points))
        result_avdiff, result = points_step(regular_points)
        assert exp_avdiff == result_avdiff
        assert result

    def test_irregular_points(self):  # noqa: D102
        irregular_points = np.array([2, 5, 1, 4])
        exp_avdiff = np.mean(np.diff(irregular_points))
        result_avdiff, result = points_step(irregular_points)
        assert exp_avdiff == result_avdiff
        assert not result

    def test_single_point(self):  # noqa: D102
        lone_point = np.array([4])
        result_avdiff, result = points_step(lone_point)
        assert np.isnan(result_avdiff)
        assert result

    def test_no_points(self):  # noqa: D102
        no_points = np.array([])
        result_avdiff, result = points_step(no_points)
        assert np.isnan(result_avdiff)
        assert result
