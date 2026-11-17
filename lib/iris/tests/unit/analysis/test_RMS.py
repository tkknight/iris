# Copyright Iris contributors
#
# This file is part of Iris and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Unit tests for the :data:`iris.analysis.RMS` aggregator."""

import numpy as np
import numpy.ma as ma
import pytest

from iris._lazy_data import as_lazy_data
from iris.analysis import RMS
from iris.tests import _shared_utils


class Test_aggregate:
    """Test aggregate."""
    def test_1d(self):  # noqa: D102
        # 1-dimensional input
        data = np.array([5, 2, 6, 4], dtype=np.float64)
        rms = RMS.aggregate(data, 0)
        expected_rms = 4.5
        assert rms == pytest.approx(expected_rms)

    def test_2d(self):  # noqa: D102
        # 2-dimensional input
        data = np.array([[5, 2, 6, 4], [12, 4, 10, 8]], dtype=np.float64)
        expected_rms = np.array([4.5, 9.0], dtype=np.float64)
        rms = RMS.aggregate(data, 1)
        _shared_utils.assert_array_almost_equal(rms, expected_rms)

    def test_1d_weighted(self):  # noqa: D102
        # 1-dimensional input with weights
        data = np.array([4, 7, 10, 8], dtype=np.float64)
        weights = np.array([1, 4, 3, 2], dtype=np.float64)
        expected_rms = 8.0
        rms = RMS.aggregate(data, 0, weights=weights)
        assert rms == pytest.approx(expected_rms)

    def test_2d_weighted(self):  # noqa: D102
        # 2-dimensional input with weights
        data = np.array([[4, 7, 10, 8], [14, 16, 20, 8]], dtype=np.float64)
        weights = np.array([[1, 4, 3, 2], [2, 1, 1.5, 0.5]], dtype=np.float64)
        expected_rms = np.array([8.0, 16.0], dtype=np.float64)
        rms = RMS.aggregate(data, 1, weights=weights)
        _shared_utils.assert_array_almost_equal(rms, expected_rms)

    def test_unit_weighted(self):  # noqa: D102
        # unit weights should be the same as no weights
        data = np.array([5, 2, 6, 4], dtype=np.float64)
        weights = np.ones_like(data)
        rms = RMS.aggregate(data, 0, weights=weights)
        expected_rms = 4.5
        assert rms == pytest.approx(expected_rms)

    def test_masked(self):  # noqa: D102
        # masked entries should be completely ignored
        data = ma.array(
            [5, 10, 2, 11, 6, 4],
            mask=[False, True, False, True, False, False],
            dtype=np.float64,
        )
        expected_rms = 4.5
        rms = RMS.aggregate(data, 0)
        assert rms == pytest.approx(expected_rms)

    def test_masked_weighted(self):  # noqa: D102
        # weights should work properly with masked arrays
        data = ma.array(
            [4, 7, 18, 10, 11, 8],
            mask=[False, False, True, False, True, False],
            dtype=np.float64,
        )
        weights = np.array([1, 4, 5, 3, 8, 2], dtype=np.float64)
        expected_rms = 8.0
        rms = RMS.aggregate(data, 0, weights=weights)
        assert rms == pytest.approx(expected_rms)


class Test_lazy_aggregate:
    """Test lazy aggregate."""
    def test_1d(self):  # noqa: D102
        # 1-dimensional input.
        data = as_lazy_data(np.array([5, 2, 6, 4], dtype=np.float64))
        rms = RMS.lazy_aggregate(data, 0)
        expected_rms = 4.5
        assert rms == pytest.approx(expected_rms)

    def test_2d(self):  # noqa: D102
        # 2-dimensional input.
        data = as_lazy_data(np.array([[5, 2, 6, 4], [12, 4, 10, 8]], dtype=np.float64))
        expected_rms = np.array([4.5, 9.0], dtype=np.float64)
        rms = RMS.lazy_aggregate(data, 1)
        _shared_utils.assert_array_almost_equal(rms, expected_rms)

    def test_1d_weighted(self):  # noqa: D102
        # 1-dimensional input with weights.
        data = as_lazy_data(np.array([4, 7, 10, 8], dtype=np.float64))
        weights = np.array([1, 4, 3, 2], dtype=np.float64)
        expected_rms = 8.0
        rms = RMS.lazy_aggregate(data, 0, weights=weights)
        assert rms == pytest.approx(expected_rms)

    def test_1d_lazy_weighted(self):  # noqa: D102
        # 1-dimensional input with lazy weights.
        data = as_lazy_data(np.array([4, 7, 10, 8], dtype=np.float64))
        weights = as_lazy_data(np.array([1, 4, 3, 2], dtype=np.float64))
        expected_rms = 8.0
        rms = RMS.lazy_aggregate(data, 0, weights=weights)
        assert rms == pytest.approx(expected_rms)

    def test_2d_weighted(self):  # noqa: D102
        # 2-dimensional input with weights.
        data = as_lazy_data(
            np.array([[4, 7, 10, 8], [14, 16, 20, 8]], dtype=np.float64)
        )
        weights = np.array([[1, 4, 3, 2], [2, 1, 1.5, 0.5]], dtype=np.float64)
        expected_rms = np.array([8.0, 16.0], dtype=np.float64)
        rms = RMS.lazy_aggregate(data, 1, weights=weights)
        _shared_utils.assert_array_almost_equal(rms, expected_rms)

    def test_unit_weighted(self):  # noqa: D102
        # Unit weights should be the same as no weights.
        data = as_lazy_data(np.array([5, 2, 6, 4], dtype=np.float64))
        weights = np.ones_like(data)
        expected_rms = 4.5
        rms = RMS.lazy_aggregate(data, 0, weights=weights)
        assert rms == pytest.approx(expected_rms)

    def test_masked(self):  # noqa: D102
        # Masked entries should be completely ignored.
        data = as_lazy_data(
            ma.array(
                [5, 10, 2, 11, 6, 4],
                mask=[False, True, False, True, False, False],
                dtype=np.float64,
            )
        )
        expected_rms = 4.5
        rms = RMS.lazy_aggregate(data, 0)
        assert rms == pytest.approx(expected_rms)

    def test_masked_weighted(self):  # noqa: D102
        data = as_lazy_data(
            ma.array(
                [4, 7, 18, 10, 11, 8],
                mask=[False, False, True, False, True, False],
                dtype=np.float64,
            )
        )
        weights = np.array([1, 4, 5, 3, 8, 2])
        expected_rms = 8.0
        rms = RMS.lazy_aggregate(data, 0, weights=weights)
        assert rms == pytest.approx(expected_rms)


class Test_name:
    """Test name."""
    def test(self):  # noqa: D102
        assert RMS.name() == "root_mean_square"


class Test_aggregate_shape:
    """Test aggregate shape."""
    def test(self):  # noqa: D102
        shape = ()
        kwargs = dict()
        assert RMS.aggregate_shape(**kwargs) == shape
        kwargs = dict(tom="jerry", calvin="hobbes")
        assert RMS.aggregate_shape(**kwargs) == shape
