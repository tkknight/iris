# Copyright Iris contributors
#
# This file is part of Iris and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Unit tests for :class:`iris.analysis.Linear`."""

import pytest

from iris.analysis import Linear


def create_scheme(mode=None):  # noqa: D103
    kwargs = {}
    if mode is not None:
        kwargs["extrapolation_mode"] = mode
    return Linear(**kwargs)


class Test_extrapolation_mode:
    """Test extrapolation mode."""
    def check_mode(self, mode):  # noqa: D102
        linear = create_scheme(mode)
        assert linear.extrapolation_mode == mode

    def test_default(self):  # noqa: D102
        linear = Linear()
        assert linear.extrapolation_mode == "linear"

    def test_extrapolate(self):  # noqa: D102
        self.check_mode("extrapolate")

    def test_linear(self):  # noqa: D102
        self.check_mode("linear")

    def test_nan(self):  # noqa: D102
        self.check_mode("nan")

    def test_error(self):  # noqa: D102
        self.check_mode("error")

    def test_mask(self):  # noqa: D102
        self.check_mode("mask")

    def test_nanmask(self):  # noqa: D102
        self.check_mode("nanmask")

    def test_invalid(self):  # noqa: D102
        with pytest.raises(ValueError, match="Extrapolation mode"):
            Linear("bogus")


class Test_interpolator:
    """Test interpolator."""
    def check_mode(self, mocker, mode=None):  # noqa: D102
        linear = create_scheme(mode)

        # Check that calling `linear.interpolator(...)` returns an
        # instance of RectilinearInterpolator which has been created
        # using the correct arguments.
        ri = mocker.patch(
            "iris.analysis.RectilinearInterpolator",
            return_value=mocker.sentinel.interpolator,
        )
        interpolator = linear.interpolator(mocker.sentinel.cube, mocker.sentinel.coords)
        if mode is None or mode == "linear":
            expected_mode = "extrapolate"
        else:
            expected_mode = mode
        ri.assert_called_once_with(
            mocker.sentinel.cube, mocker.sentinel.coords, "linear", expected_mode
        )
        assert interpolator is mocker.sentinel.interpolator

    def test_default(self, mocker):  # noqa: D102
        self.check_mode(mocker)

    def test_extrapolate(self, mocker):  # noqa: D102
        self.check_mode(mocker, "extrapolate")

    def test_linear(self, mocker):  # noqa: D102
        self.check_mode(mocker, "linear")

    def test_nan(self, mocker):  # noqa: D102
        self.check_mode(mocker, "nan")

    def test_error(self, mocker):  # noqa: D102
        self.check_mode(mocker, "error")

    def test_mask(self, mocker):  # noqa: D102
        self.check_mode(mocker, "mask")

    def test_nanmask(self, mocker):  # noqa: D102
        self.check_mode(mocker, "nanmask")


class Test_regridder:
    """Test regridder."""
    def check_mode(self, mocker, mode=None):  # noqa: D102
        linear = create_scheme(mode)

        # Check that calling `linear.regridder(...)` returns an instance
        # of RectilinearRegridder which has been created using the correct
        # arguments.
        lr = mocker.patch(
            "iris.analysis.RectilinearRegridder",
            return_value=mocker.sentinel.regridder,
        )
        regridder = linear.regridder(mocker.sentinel.src, mocker.sentinel.target)
        if mode is None or mode == "linear":
            expected_mode = "extrapolate"
        else:
            expected_mode = mode
        lr.assert_called_once_with(
            mocker.sentinel.src, mocker.sentinel.target, "linear", expected_mode
        )
        assert regridder is mocker.sentinel.regridder

    def test_default(self, mocker):  # noqa: D102
        self.check_mode(mocker)

    def test_extrapolate(self, mocker):  # noqa: D102
        self.check_mode(mocker, "extrapolate")

    def test_linear(self, mocker):  # noqa: D102
        self.check_mode(mocker, "linear")

    def test_nan(self, mocker):  # noqa: D102
        self.check_mode(mocker, "nan")

    def test_error(self, mocker):  # noqa: D102
        self.check_mode(mocker, "error")

    def test_mask(self, mocker):  # noqa: D102
        self.check_mode(mocker, "mask")

    def test_nanmask(self, mocker):  # noqa: D102
        self.check_mode(mocker, "nanmask")
