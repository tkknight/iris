# Copyright Iris contributors
#
# This file is part of Iris and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Unit tests for the `iris.config.NetCDF` class."""

import re
import warnings

import pytest

import iris.config


@pytest.fixture
def options():  # noqa: D103
    return iris.config.NetCDF()


def test_basic(options):  # noqa: D103
    assert not options.conventions_override


def test_enabled(options):  # noqa: D103
    options.conventions_override = True
    assert options.conventions_override


def test_bad_value(options):  # noqa: D103
    # A bad value should be ignored and replaced with the default value.
    bad_value = "wibble"
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        options.conventions_override = bad_value
    assert not options.conventions_override
    exp_wmsg = "Attempting to set invalid value {!r}".format(bad_value)
    assert re.match(exp_wmsg, str(w[0].message))


def test__contextmgr(options):  # noqa: D103
    with options.context(conventions_override=True):
        assert options.conventions_override
    assert not options.conventions_override
