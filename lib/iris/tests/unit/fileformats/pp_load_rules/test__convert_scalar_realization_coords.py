# Copyright Iris contributors
#
# This file is part of Iris and is released under the LGPL license.
# See COPYING and COPYING.LESSER in the root of the repository for full
# licensing details.
"""
Unit tests for
:func:`iris.fileformats.pp_load_rules._convert_scalar_realization_coords`.

"""

# Import iris.tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests  # isort:skip

from iris.coords import DimCoord
from iris.fileformats.pp_load_rules import _convert_scalar_realization_coords
from iris.tests.unit.fileformats import TestField


class Test(TestField):
    def test_valid(self):
        coords_and_dims = _convert_scalar_realization_coords(lbrsvd4=21)
        self.assertEqual(
            coords_and_dims,
            [(DimCoord([21], standard_name="realization", units="1"), None)],
        )

    def test_missing_indicator(self):
        coords_and_dims = _convert_scalar_realization_coords(lbrsvd4=0)
        self.assertEqual(coords_and_dims, [])


if __name__ == "__main__":
    tests.main()
