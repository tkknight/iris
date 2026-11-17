# Copyright Iris contributors
#
# This file is part of Iris and is released under the BSD license.
# See LICENSE in the root of the repository for full licensing details.
"""Mirror of :mod:`iris.tests.unit.fileformats.netcdf.test_Saver`, but with lazy arrays."""

from types import ModuleType

from dask import array as da
import pytest

from iris.coords import AuxCoord
from iris.fileformats.netcdf import Saver
from iris.tests import _shared_utils, stock
from iris.tests.unit.fileformats.netcdf.saver import test_Saver


class LazyMixin:
    """LazyMixin."""
    array_lib: ModuleType = da

    @pytest.fixture(autouse=True)
    def _setup_lazy_mixin(self, monkeypatch):
        rp = _shared_utils.result_path

        def _result_path(request, basename=None, ext=""):
            # Precisely mirroring the tests in test_Saver, so use those CDL's.
            original = rp(request, basename, ext)
            return original.replace("Saver__lazy", "Saver")

        monkeypatch.setattr(
            "iris.tests._shared_utils.result_path",  # IMPORTANT: patch where it is USED
            _result_path,
        )


class Test_write(LazyMixin, test_Saver.Test_write):
    """Test write."""
    pass


class Test__create_cf_bounds(test_Saver.Test__create_cf_bounds):
    """Test  create cf bounds."""
    @staticmethod
    def climatology_3d():  # noqa: D102
        cube = stock.climatology_3d()
        aux_coord = AuxCoord.from_coord(cube.coord("time"))
        lazy_coord = aux_coord.copy(aux_coord.lazy_points(), aux_coord.lazy_bounds())
        cube.replace_coord(lazy_coord)
        return cube


class Test_write__valid_x_cube_attributes(
    LazyMixin, test_Saver.Test_write__valid_x_cube_attributes
):
    """Test write  valid x cube attributes."""
    pass


class Test_write__valid_x_coord_attributes(
    LazyMixin, test_Saver.Test_write__valid_x_coord_attributes
):
    """Test write  valid x coord attributes."""
    pass


class Test_write_fill_value(LazyMixin, test_Saver.Test_write_fill_value):
    """Test write fill value."""
    pass


class Test_check_attribute_compliance__valid_range(
    LazyMixin, test_Saver.Test_check_attribute_compliance__valid_range
):
    """Test check attribute compliance  valid range."""
    pass


class Test_check_attribute_compliance__valid_min(
    LazyMixin, test_Saver.Test_check_attribute_compliance__valid_min
):
    """Test check attribute compliance  valid min."""
    pass


class Test_check_attribute_compliance__valid_max(
    LazyMixin, test_Saver.Test_check_attribute_compliance__valid_max
):
    """Test check attribute compliance  valid max."""
    pass


class Test_check_attribute_compliance__exception_handling(
    LazyMixin, test_Saver.Test_check_attribute_compliance__exception_handling
):
    """Test check attribute compliance  exception handling."""
    pass


class TestStreamed:
    """Test treamed."""
    @pytest.fixture(autouse=True)
    def _setup(self, mocker):
        self.cube = stock.simple_2d()
        self.store_watch = mocker.patch("dask.array.store")

    @pytest.fixture
    def save_common(self, tmp_path):  # noqa: D102
        def _save_common(cube_to_save):
            nc_path = tmp_path / "temp.nc"
            with Saver(nc_path, "NETCDF4") as saver:
                saver.write(cube_to_save)

        return _save_common

    def test_realised_not_streamed(self, save_common):  # noqa: D102
        save_common(self.cube)
        assert not self.store_watch.called

    def test_lazy_streamed_data(self, save_common):  # noqa: D102
        self.cube.data = self.cube.lazy_data()
        save_common(self.cube)
        assert self.store_watch.called

    def test_lazy_streamed_coord(self, save_common):  # noqa: D102
        aux_coord = AuxCoord.from_coord(self.cube.coords()[0])
        lazy_coord = aux_coord.copy(aux_coord.lazy_points(), aux_coord.lazy_bounds())
        self.cube.replace_coord(lazy_coord)
        save_common(self.cube)
        assert self.store_watch.called

    def test_lazy_streamed_bounds(self, save_common):  # noqa: D102
        aux_coord = AuxCoord.from_coord(self.cube.coords()[0])
        lazy_coord = aux_coord.copy(aux_coord.points, aux_coord.lazy_bounds())
        self.cube.replace_coord(lazy_coord)
        save_common(self.cube)
        assert self.store_watch.called
