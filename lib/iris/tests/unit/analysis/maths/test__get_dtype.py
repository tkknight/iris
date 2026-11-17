# Copyright Iris contributors
#
# This file is part of Iris and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Unit tests for the function :func:`iris.analysis.maths._get_dtype`."""

import numpy as np
from numpy import ma

from iris.analysis.maths import _get_dtype
from iris.coords import AuxCoord, DimCoord
from iris.cube import Cube


class TestGetDtype:
    """Test etDtype."""
    def _check_call(self, obj, expected_dtype):
        result = _get_dtype(obj)
        assert expected_dtype == result

    def test_int8(self):  # noqa: D102
        n = -128
        self._check_call(n, np.int8)

    def test_int16(self):  # noqa: D102
        n = -129
        self._check_call(n, np.int16)

    def test_uint8(self):  # noqa: D102
        n = 255
        self._check_call(n, np.uint8)

    def test_uint16(self):  # noqa: D102
        n = 256
        self._check_call(n, np.uint16)

    def test_float16(self):  # noqa: D102
        n = 60000.0
        self._check_call(n, np.float16)

    def test_float32(self):  # noqa: D102
        n = 65000.0
        self._check_call(n, np.float32)

    def test_float64(self):  # noqa: D102
        n = 1e40
        self._check_call(n, np.float64)

    def test_scalar_demote(self):  # noqa: D102
        n = np.int64(10)
        self._check_call(n, np.uint8)

    def test_array(self):  # noqa: D102
        a = np.array([1, 2, 3], dtype=np.int16)
        self._check_call(a, np.int16)

    def test_scalar_array(self):  # noqa: D102
        dtype = np.int32
        a = np.array(1, dtype=dtype)
        self._check_call(a, dtype)

    def test_masked_array(self):  # noqa: D102
        dtype = np.float16
        m = ma.masked_array([1, 2, 3], [1, 0, 1], dtype=dtype)
        self._check_call(m, dtype)

    def test_masked_constant(self):  # noqa: D102
        m = ma.masked
        self._check_call(m, m.dtype)

    def test_cube(self):  # noqa: D102
        dtype = np.float32
        data = np.array([1, 2, 3], dtype=dtype)
        cube = Cube(data)
        self._check_call(cube, dtype)

    def test_aux_coord(self):  # noqa: D102
        dtype = np.int64
        points = np.array([1, 2, 3], dtype=dtype)
        aux_coord = AuxCoord(points)
        self._check_call(aux_coord, dtype)

    def test_dim_coord(self):  # noqa: D102
        dtype = np.float16
        points = np.array([1, 2, 3], dtype=dtype)
        dim_coord = DimCoord(points)
        self._check_call(dim_coord, dtype)
