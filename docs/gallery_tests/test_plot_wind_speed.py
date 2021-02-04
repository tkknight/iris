# Copyright Iris contributors
#
# This file is part of Iris and is released under the LGPL license.
# See COPYING and COPYING.LESSER in the root of the repository for full
# licensing details.

# Import Iris tests first so that some things can be initialised before
# importing anything else.
import iris.tests as tests

from .gallerytest_util import (
    add_gallery_to_path,
    show_replaced_by_check_graphic,
    fail_any_deprecation_warnings,
)


class TestWindSpeed(tests.GraphicsTest):
    """Test the wind_speed gallery code."""

    def test_plot_wind_speed(self):
        with fail_any_deprecation_warnings():
            with add_gallery_to_path():
                import plot_wind_speed
            with show_replaced_by_check_graphic(self):
                plot_wind_speed.main()


if __name__ == "__main__":
    tests.main()
