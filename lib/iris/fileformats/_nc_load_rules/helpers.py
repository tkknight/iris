# Copyright Iris contributors
#
# This file is part of Iris and is released under the LGPL license.
# See COPYING and COPYING.LESSER in the root of the repository for full
# licensing details.
"""
All the pure-Python 'helper' functions which were previously included in the
Pyke rules database 'fc_rules_cf.krb'.

The 'action' routines now call these, as the rules used to do.
They have not changed, **except** that the 'build_coordinate_system' routine
acquired an extra initial 'engine' argument, purely for consistency with other
build routines, and which it does not use.

"""

import warnings

import cf_units
import numpy as np
import numpy.ma as ma

import iris.aux_factory
from iris.common.mixin import _get_valid_standard_name
import iris.coord_systems
import iris.coords
import iris.exceptions
import iris.fileformats.cf as cf
import iris.fileformats.netcdf
from iris.fileformats.netcdf import (
    UnknownCellMethodWarning,
    _get_cf_var_data,
    parse_cell_methods,
)
import iris.std_names
import iris.util

#
# UD Units Constants (based on Unidata udunits.dat definition file)
#
UD_UNITS_LAT = [
    "degrees_north",
    "degree_north",
    "degree_n",
    "degrees_n",
    "degreen",
    "degreesn",
    "degrees",
    "degrees north",
    "degree north",
    "degree n",
    "degrees n",
]
UD_UNITS_LON = [
    "degrees_east",
    "degree_east",
    "degree_e",
    "degrees_e",
    "degreee",
    "degreese",
    "degrees",
    "degrees east",
    "degree east",
    "degree e",
    "degrees e",
]
UNKNOWN_UNIT_STRING = "?"
NO_UNIT_STRING = "-"

#
# CF Dimensionless Vertical Coordinates
#
CF_COORD_VERTICAL = {
    "atmosphere_ln_pressure_coordinate": ["p0", "lev"],
    "atmosphere_sigma_coordinate": ["sigma", "ps", "ptop"],
    "atmosphere_hybrid_sigma_pressure_coordinate": ["a", "b", "ps", "p0"],
    "atmosphere_hybrid_height_coordinate": ["a", "b", "orog"],
    "atmosphere_sleve_coordinate": [
        "a",
        "b1",
        "b2",
        "ztop",
        "zsurf1",
        "zsurf2",
    ],
    "ocean_sigma_coordinate": ["sigma", "eta", "depth"],
    "ocean_s_coordinate": ["s", "eta", "depth", "a", "b", "depth_c"],
    "ocean_sigma_z_coordinate": [
        "sigma",
        "eta",
        "depth",
        "depth_c",
        "nsigma",
        "zlev",
    ],
    "ocean_double_sigma_coordinate": [
        "sigma",
        "depth",
        "z1",
        "z2",
        "a",
        "href",
        "k_c",
    ],
    "ocean_s_coordinate_g1": ["s", "eta", "depth", "depth_c", "C"],
    "ocean_s_coordinate_g2": ["s", "eta", "depth", "depth_c", "C"],
}

#
# CF Grid Mappings
#
CF_GRID_MAPPING_ALBERS = "albers_conical_equal_area"
CF_GRID_MAPPING_AZIMUTHAL = "azimuthal_equidistant"
CF_GRID_MAPPING_LAMBERT_AZIMUTHAL = "lambert_azimuthal_equal_area"
CF_GRID_MAPPING_LAMBERT_CONFORMAL = "lambert_conformal_conic"
CF_GRID_MAPPING_LAMBERT_CYLINDRICAL = "lambert_cylindrical_equal_area"
CF_GRID_MAPPING_LAT_LON = "latitude_longitude"
CF_GRID_MAPPING_MERCATOR = "mercator"
CF_GRID_MAPPING_ORTHO = "orthographic"
CF_GRID_MAPPING_POLAR = "polar_stereographic"
CF_GRID_MAPPING_ROTATED_LAT_LON = "rotated_latitude_longitude"
CF_GRID_MAPPING_STEREO = "stereographic"
CF_GRID_MAPPING_TRANSVERSE = "transverse_mercator"
CF_GRID_MAPPING_VERTICAL = "vertical_perspective"
CF_GRID_MAPPING_GEOSTATIONARY = "geostationary"

#
# CF Attribute Names.
#
CF_ATTR_AXIS = "axis"
CF_ATTR_BOUNDS = "bounds"
CF_ATTR_CALENDAR = "calendar"
CF_ATTR_CLIMATOLOGY = "climatology"
CF_ATTR_GRID_INVERSE_FLATTENING = "inverse_flattening"
CF_ATTR_GRID_EARTH_RADIUS = "earth_radius"
CF_ATTR_GRID_MAPPING_NAME = "grid_mapping_name"
CF_ATTR_GRID_NORTH_POLE_LAT = "grid_north_pole_latitude"
CF_ATTR_GRID_NORTH_POLE_LON = "grid_north_pole_longitude"
CF_ATTR_GRID_NORTH_POLE_GRID_LON = "north_pole_grid_longitude"
CF_ATTR_GRID_SEMI_MAJOR_AXIS = "semi_major_axis"
CF_ATTR_GRID_SEMI_MINOR_AXIS = "semi_minor_axis"
CF_ATTR_GRID_LAT_OF_PROJ_ORIGIN = "latitude_of_projection_origin"
CF_ATTR_GRID_LON_OF_PROJ_ORIGIN = "longitude_of_projection_origin"
CF_ATTR_GRID_STANDARD_PARALLEL = "standard_parallel"
CF_ATTR_GRID_FALSE_EASTING = "false_easting"
CF_ATTR_GRID_FALSE_NORTHING = "false_northing"
CF_ATTR_GRID_SCALE_FACTOR_AT_PROJ_ORIGIN = "scale_factor_at_projection_origin"
CF_ATTR_GRID_SCALE_FACTOR_AT_CENT_MERIDIAN = "scale_factor_at_central_meridian"
CF_ATTR_GRID_LON_OF_CENT_MERIDIAN = "longitude_of_central_meridian"
CF_ATTR_GRID_STANDARD_PARALLEL = "standard_parallel"
CF_ATTR_GRID_PERSPECTIVE_HEIGHT = "perspective_point_height"
CF_ATTR_GRID_SWEEP_ANGLE_AXIS = "sweep_angle_axis"
CF_ATTR_POSITIVE = "positive"
CF_ATTR_STD_NAME = "standard_name"
CF_ATTR_LONG_NAME = "long_name"
CF_ATTR_UNITS = "units"
CF_ATTR_CELL_METHODS = "cell_methods"

#
# CF Attribute Value Constants.
#
# Attribute - axis.
CF_VALUE_AXIS_X = "x"
CF_VALUE_AXIS_Y = "y"
CF_VALUE_AXIS_T = "t"
CF_VALUE_AXIS_Z = "z"


# Attribute - positive.
CF_VALUE_POSITIVE = ["down", "up"]

# Attribute - standard_name.
CF_VALUE_STD_NAME_LAT = "latitude"
CF_VALUE_STD_NAME_LON = "longitude"
CF_VALUE_STD_NAME_GRID_LAT = "grid_latitude"
CF_VALUE_STD_NAME_GRID_LON = "grid_longitude"
CF_VALUE_STD_NAME_PROJ_X = "projection_x_coordinate"
CF_VALUE_STD_NAME_PROJ_Y = "projection_y_coordinate"


################################################################################
def build_cube_metadata(engine):
    """Add the standard meta data to the cube."""

    cf_var = engine.cf_var
    cube = engine.cube

    # Determine the cube's name attributes
    cube.var_name = cf_var.cf_name
    standard_name = getattr(cf_var, CF_ATTR_STD_NAME, None)
    long_name = getattr(cf_var, CF_ATTR_LONG_NAME, None)
    cube.long_name = long_name

    if standard_name is not None:
        try:
            cube.standard_name = _get_valid_standard_name(standard_name)
        except ValueError:
            if cube.long_name is not None:
                cube.attributes["invalid_standard_name"] = standard_name
            else:
                cube.long_name = standard_name

    # Determine the cube units.
    attr_units = get_attr_units(cf_var, cube.attributes)
    cube.units = attr_units

    # Incorporate cell methods
    nc_att_cell_methods = getattr(cf_var, CF_ATTR_CELL_METHODS, None)
    with warnings.catch_warnings(record=True) as warning_records:
        cube.cell_methods = parse_cell_methods(nc_att_cell_methods)
    # Filter to get the warning we are interested in.
    warning_records = [
        record
        for record in warning_records
        if issubclass(record.category, UnknownCellMethodWarning)
    ]
    if len(warning_records) > 0:
        # Output an enhanced warning message.
        warn_record = warning_records[0]
        name = "{}".format(cf_var.cf_name)
        msg = warn_record.message.args[0]
        msg = msg.replace("variable", "variable {!r}".format(name))
        warnings.warn(message=msg, category=UnknownCellMethodWarning)

    # Set the cube global attributes.
    for attr_name, attr_value in cf_var.cf_group.global_attributes.items():
        try:
            cube.attributes[str(attr_name)] = attr_value
        except ValueError as e:
            msg = "Skipping global attribute {!r}: {}"
            warnings.warn(msg.format(attr_name, str(e)))


################################################################################
def _get_ellipsoid(cf_grid_var):
    """Return the ellipsoid definition."""
    major = getattr(cf_grid_var, CF_ATTR_GRID_SEMI_MAJOR_AXIS, None)
    minor = getattr(cf_grid_var, CF_ATTR_GRID_SEMI_MINOR_AXIS, None)
    inverse_flattening = getattr(
        cf_grid_var, CF_ATTR_GRID_INVERSE_FLATTENING, None
    )

    # Avoid over-specification exception.
    if major is not None and minor is not None:
        inverse_flattening = None

    # Check for a default spherical earth.
    if major is None and minor is None and inverse_flattening is None:
        major = getattr(cf_grid_var, CF_ATTR_GRID_EARTH_RADIUS, None)

    return major, minor, inverse_flattening


################################################################################
def build_coordinate_system(engine, cf_grid_var):
    """Create a coordinate system from the CF-netCDF grid mapping variable."""
    major, minor, inverse_flattening = _get_ellipsoid(cf_grid_var)

    return iris.coord_systems.GeogCS(major, minor, inverse_flattening)


################################################################################
def build_rotated_coordinate_system(engine, cf_grid_var):
    """Create a rotated coordinate system from the CF-netCDF grid mapping variable."""
    major, minor, inverse_flattening = _get_ellipsoid(cf_grid_var)

    north_pole_latitude = getattr(
        cf_grid_var, CF_ATTR_GRID_NORTH_POLE_LAT, 90.0
    )
    north_pole_longitude = getattr(
        cf_grid_var, CF_ATTR_GRID_NORTH_POLE_LON, 0.0
    )
    if north_pole_latitude is None or north_pole_longitude is None:
        warnings.warn("Rotated pole position is not fully specified")

    north_pole_grid_lon = getattr(
        cf_grid_var, CF_ATTR_GRID_NORTH_POLE_GRID_LON, 0.0
    )

    ellipsoid = None
    if (
        major is not None
        or minor is not None
        or inverse_flattening is not None
    ):
        ellipsoid = iris.coord_systems.GeogCS(major, minor, inverse_flattening)

    rcs = iris.coord_systems.RotatedGeogCS(
        north_pole_latitude,
        north_pole_longitude,
        north_pole_grid_lon,
        ellipsoid,
    )

    return rcs


################################################################################
def build_transverse_mercator_coordinate_system(engine, cf_grid_var):
    """
    Create a transverse Mercator coordinate system from the CF-netCDF
    grid mapping variable.

    """
    major, minor, inverse_flattening = _get_ellipsoid(cf_grid_var)

    latitude_of_projection_origin = getattr(
        cf_grid_var, CF_ATTR_GRID_LAT_OF_PROJ_ORIGIN, None
    )
    longitude_of_central_meridian = getattr(
        cf_grid_var, CF_ATTR_GRID_LON_OF_CENT_MERIDIAN, None
    )
    false_easting = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_EASTING, None)
    false_northing = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_NORTHING, None)
    scale_factor_at_central_meridian = getattr(
        cf_grid_var, CF_ATTR_GRID_SCALE_FACTOR_AT_CENT_MERIDIAN, None
    )

    # The following accounts for the inconsistancy in the transverse
    # mercator description within the CF spec.
    if longitude_of_central_meridian is None:
        longitude_of_central_meridian = getattr(
            cf_grid_var, CF_ATTR_GRID_LON_OF_PROJ_ORIGIN, None
        )
    if scale_factor_at_central_meridian is None:
        scale_factor_at_central_meridian = getattr(
            cf_grid_var, CF_ATTR_GRID_SCALE_FACTOR_AT_PROJ_ORIGIN, None
        )

    ellipsoid = None
    if (
        major is not None
        or minor is not None
        or inverse_flattening is not None
    ):
        ellipsoid = iris.coord_systems.GeogCS(major, minor, inverse_flattening)

    cs = iris.coord_systems.TransverseMercator(
        latitude_of_projection_origin,
        longitude_of_central_meridian,
        false_easting,
        false_northing,
        scale_factor_at_central_meridian,
        ellipsoid,
    )

    return cs


################################################################################
def build_lambert_conformal_coordinate_system(engine, cf_grid_var):
    """
    Create a Lambert conformal conic coordinate system from the CF-netCDF
    grid mapping variable.

    """
    major, minor, inverse_flattening = _get_ellipsoid(cf_grid_var)

    latitude_of_projection_origin = getattr(
        cf_grid_var, CF_ATTR_GRID_LAT_OF_PROJ_ORIGIN, None
    )
    longitude_of_central_meridian = getattr(
        cf_grid_var, CF_ATTR_GRID_LON_OF_CENT_MERIDIAN, None
    )
    false_easting = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_EASTING, None)
    false_northing = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_NORTHING, None)
    standard_parallel = getattr(
        cf_grid_var, CF_ATTR_GRID_STANDARD_PARALLEL, None
    )

    ellipsoid = None
    if (
        major is not None
        or minor is not None
        or inverse_flattening is not None
    ):
        ellipsoid = iris.coord_systems.GeogCS(major, minor, inverse_flattening)

    cs = iris.coord_systems.LambertConformal(
        latitude_of_projection_origin,
        longitude_of_central_meridian,
        false_easting,
        false_northing,
        standard_parallel,
        ellipsoid,
    )

    return cs


################################################################################
def build_stereographic_coordinate_system(engine, cf_grid_var):
    """
    Create a stereographic coordinate system from the CF-netCDF
    grid mapping variable.

    """
    major, minor, inverse_flattening = _get_ellipsoid(cf_grid_var)

    latitude_of_projection_origin = getattr(
        cf_grid_var, CF_ATTR_GRID_LAT_OF_PROJ_ORIGIN, None
    )
    longitude_of_projection_origin = getattr(
        cf_grid_var, CF_ATTR_GRID_LON_OF_PROJ_ORIGIN, None
    )
    false_easting = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_EASTING, None)
    false_northing = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_NORTHING, None)
    # Iris currently only supports Stereographic projections with a scale
    # factor of 1.0. This is checked elsewhere.

    ellipsoid = None
    if (
        major is not None
        or minor is not None
        or inverse_flattening is not None
    ):
        ellipsoid = iris.coord_systems.GeogCS(major, minor, inverse_flattening)

    cs = iris.coord_systems.Stereographic(
        latitude_of_projection_origin,
        longitude_of_projection_origin,
        false_easting,
        false_northing,
        true_scale_lat=None,
        ellipsoid=ellipsoid,
    )

    return cs


################################################################################
def build_mercator_coordinate_system(engine, cf_grid_var):
    """
    Create a Mercator coordinate system from the CF-netCDF
    grid mapping variable.

    """
    major, minor, inverse_flattening = _get_ellipsoid(cf_grid_var)

    longitude_of_projection_origin = getattr(
        cf_grid_var, CF_ATTR_GRID_LON_OF_PROJ_ORIGIN, None
    )
    # Iris currently only supports Mercator projections with specific
    # values for false_easting, false_northing,
    # scale_factor_at_projection_origin and standard_parallel. These are
    # checked elsewhere.

    ellipsoid = None
    if (
        major is not None
        or minor is not None
        or inverse_flattening is not None
    ):
        ellipsoid = iris.coord_systems.GeogCS(major, minor, inverse_flattening)

    cs = iris.coord_systems.Mercator(
        longitude_of_projection_origin, ellipsoid=ellipsoid
    )

    return cs


################################################################################
def build_lambert_azimuthal_equal_area_coordinate_system(engine, cf_grid_var):
    """
    Create a lambert azimuthal equal area coordinate system from the CF-netCDF
    grid mapping variable.

    """
    major, minor, inverse_flattening = _get_ellipsoid(cf_grid_var)

    latitude_of_projection_origin = getattr(
        cf_grid_var, CF_ATTR_GRID_LAT_OF_PROJ_ORIGIN, None
    )
    longitude_of_projection_origin = getattr(
        cf_grid_var, CF_ATTR_GRID_LON_OF_PROJ_ORIGIN, None
    )
    false_easting = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_EASTING, None)
    false_northing = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_NORTHING, None)

    ellipsoid = None
    if (
        major is not None
        or minor is not None
        or inverse_flattening is not None
    ):
        ellipsoid = iris.coord_systems.GeogCS(major, minor, inverse_flattening)

    cs = iris.coord_systems.LambertAzimuthalEqualArea(
        latitude_of_projection_origin,
        longitude_of_projection_origin,
        false_easting,
        false_northing,
        ellipsoid,
    )

    return cs


################################################################################
def build_albers_equal_area_coordinate_system(engine, cf_grid_var):
    """
    Create a albers conical equal area coordinate system from the CF-netCDF
    grid mapping variable.

    """
    major, minor, inverse_flattening = _get_ellipsoid(cf_grid_var)

    latitude_of_projection_origin = getattr(
        cf_grid_var, CF_ATTR_GRID_LAT_OF_PROJ_ORIGIN, None
    )
    longitude_of_central_meridian = getattr(
        cf_grid_var, CF_ATTR_GRID_LON_OF_CENT_MERIDIAN, None
    )
    false_easting = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_EASTING, None)
    false_northing = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_NORTHING, None)
    standard_parallels = getattr(
        cf_grid_var, CF_ATTR_GRID_STANDARD_PARALLEL, None
    )

    ellipsoid = None
    if (
        major is not None
        or minor is not None
        or inverse_flattening is not None
    ):
        ellipsoid = iris.coord_systems.GeogCS(major, minor, inverse_flattening)

    cs = iris.coord_systems.AlbersEqualArea(
        latitude_of_projection_origin,
        longitude_of_central_meridian,
        false_easting,
        false_northing,
        standard_parallels,
        ellipsoid,
    )

    return cs


################################################################################
def build_vertical_perspective_coordinate_system(engine, cf_grid_var):
    """
    Create a vertical perspective coordinate system from the CF-netCDF
    grid mapping variable.

    """
    major, minor, inverse_flattening = _get_ellipsoid(cf_grid_var)

    latitude_of_projection_origin = getattr(
        cf_grid_var, CF_ATTR_GRID_LAT_OF_PROJ_ORIGIN, None
    )
    longitude_of_projection_origin = getattr(
        cf_grid_var, CF_ATTR_GRID_LON_OF_PROJ_ORIGIN, None
    )
    perspective_point_height = getattr(
        cf_grid_var, CF_ATTR_GRID_PERSPECTIVE_HEIGHT, None
    )
    false_easting = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_EASTING, None)
    false_northing = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_NORTHING, None)

    ellipsoid = None
    if (
        major is not None
        or minor is not None
        or inverse_flattening is not None
    ):
        ellipsoid = iris.coord_systems.GeogCS(major, minor, inverse_flattening)

    cs = iris.coord_systems.VerticalPerspective(
        latitude_of_projection_origin,
        longitude_of_projection_origin,
        perspective_point_height,
        false_easting,
        false_northing,
        ellipsoid,
    )

    return cs


################################################################################
def build_geostationary_coordinate_system(engine, cf_grid_var):
    """
    Create a geostationary coordinate system from the CF-netCDF
    grid mapping variable.

    """
    major, minor, inverse_flattening = _get_ellipsoid(cf_grid_var)

    latitude_of_projection_origin = getattr(
        cf_grid_var, CF_ATTR_GRID_LAT_OF_PROJ_ORIGIN, None
    )
    longitude_of_projection_origin = getattr(
        cf_grid_var, CF_ATTR_GRID_LON_OF_PROJ_ORIGIN, None
    )
    perspective_point_height = getattr(
        cf_grid_var, CF_ATTR_GRID_PERSPECTIVE_HEIGHT, None
    )
    false_easting = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_EASTING, None)
    false_northing = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_NORTHING, None)
    sweep_angle_axis = getattr(
        cf_grid_var, CF_ATTR_GRID_SWEEP_ANGLE_AXIS, None
    )

    ellipsoid = None
    if (
        major is not None
        or minor is not None
        or inverse_flattening is not None
    ):
        ellipsoid = iris.coord_systems.GeogCS(major, minor, inverse_flattening)

    cs = iris.coord_systems.Geostationary(
        latitude_of_projection_origin,
        longitude_of_projection_origin,
        perspective_point_height,
        sweep_angle_axis,
        false_easting,
        false_northing,
        ellipsoid,
    )

    return cs


################################################################################
def get_attr_units(cf_var, attributes):
    attr_units = getattr(cf_var, CF_ATTR_UNITS, UNKNOWN_UNIT_STRING)
    if not attr_units:
        attr_units = UNKNOWN_UNIT_STRING

    # Sanitise lat/lon units.
    if attr_units in UD_UNITS_LAT or attr_units in UD_UNITS_LON:
        attr_units = "degrees"

    # Graceful loading of invalid units.
    try:
        cf_units.as_unit(attr_units)
    except ValueError:
        # Using converted unicode message. Can be reverted with Python 3.
        msg = "Ignoring netCDF variable {!r} invalid units {!r}".format(
            cf_var.cf_name, attr_units
        )
        warnings.warn(msg)
        attributes["invalid_units"] = attr_units
        attr_units = UNKNOWN_UNIT_STRING

    if np.issubdtype(cf_var.dtype, np.str_):
        attr_units = NO_UNIT_STRING

    if any(
        hasattr(cf_var.cf_data, name)
        for name in ("flag_values", "flag_masks", "flag_meanings")
    ):
        attr_units = cf_units._NO_UNIT_STRING

    # Get any assoicated calendar for a time reference coordinate.
    if cf_units.as_unit(attr_units).is_time_reference():
        attr_calendar = getattr(cf_var, CF_ATTR_CALENDAR, None)

        if attr_calendar:
            attr_units = cf_units.Unit(attr_units, calendar=attr_calendar)

    return attr_units


################################################################################
def get_names(cf_coord_var, coord_name, attributes):
    """Determine the standard_name, long_name and var_name attributes."""

    standard_name = getattr(cf_coord_var, CF_ATTR_STD_NAME, None)
    long_name = getattr(cf_coord_var, CF_ATTR_LONG_NAME, None)
    cf_name = str(cf_coord_var.cf_name)

    if standard_name is not None:
        try:
            standard_name = _get_valid_standard_name(standard_name)
        except ValueError:
            if long_name is not None:
                attributes["invalid_standard_name"] = standard_name
                if coord_name is not None:
                    standard_name = coord_name
                else:
                    standard_name = None
            else:
                if coord_name is not None:
                    attributes["invalid_standard_name"] = standard_name
                    standard_name = coord_name
                else:
                    standard_name = None

    else:
        if coord_name is not None:
            standard_name = coord_name

    # Last attempt to set the standard name to something meaningful.
    if standard_name is None:
        if cf_name in iris.std_names.STD_NAMES:
            standard_name = cf_name

    return (standard_name, long_name, cf_name)


################################################################################
def get_cf_bounds_var(cf_coord_var):
    """
    Return the CF variable representing the bounds of a coordinate
    variable.

    """
    attr_bounds = getattr(cf_coord_var, CF_ATTR_BOUNDS, None)
    attr_climatology = getattr(cf_coord_var, CF_ATTR_CLIMATOLOGY, None)

    # Determine bounds, prefering standard bounds over climatology.
    # NB. No need to raise a warning if the bounds/climatology
    # variable is missing, as that will already have been done by
    # iris.fileformats.cf.
    cf_bounds_var = None
    climatological = False
    if attr_bounds is not None:
        bounds_vars = cf_coord_var.cf_group.bounds
        if attr_bounds in bounds_vars:
            cf_bounds_var = bounds_vars[attr_bounds]
    elif attr_climatology is not None:
        climatology_vars = cf_coord_var.cf_group.climatology
        if attr_climatology in climatology_vars:
            cf_bounds_var = climatology_vars[attr_climatology]
            climatological = True

    if attr_bounds is not None and attr_climatology is not None:
        warnings.warn(
            "Ignoring climatology in favour of bounds attribute "
            "on NetCDF variable {!r}.".format(cf_coord_var.cf_name)
        )

    return cf_bounds_var, climatological


################################################################################
def reorder_bounds_data(bounds_data, cf_bounds_var, cf_coord_var):
    """
    Return a bounds_data array with the vertex dimension as the most
    rapidly varying.

    .. note::

        This function assumes the dimension names of the coordinate
        variable match those of the bounds variable in order to determine
        which is the vertex dimension.


    """
    vertex_dim_names = set(cf_bounds_var.dimensions).difference(
        cf_coord_var.dimensions
    )
    if len(vertex_dim_names) != 1:
        msg = (
            "Too many dimension names differ between coordinate "
            "variable {!r} and the bounds variable {!r}. "
            "Expected 1, got {}."
        )
        raise ValueError(
            msg.format(
                str(cf_coord_var.cf_name),
                str(cf_bounds_var.cf_name),
                len(vertex_dim_names),
            )
        )
    vertex_dim = cf_bounds_var.dimensions.index(*vertex_dim_names)
    bounds_data = np.rollaxis(
        bounds_data.view(), vertex_dim, len(bounds_data.shape)
    )
    return bounds_data


################################################################################
def build_dimension_coordinate(
    engine, cf_coord_var, coord_name=None, coord_system=None
):
    """Create a dimension coordinate (DimCoord) and add it to the cube."""

    cf_var = engine.cf_var
    cube = engine.cube
    attributes = {}

    attr_units = get_attr_units(cf_coord_var, attributes)
    points_data = cf_coord_var[:]
    # Gracefully fill points masked array.
    if ma.is_masked(points_data):
        points_data = ma.filled(points_data)
        msg = "Gracefully filling {!r} dimension coordinate masked points"
        warnings.warn(msg.format(str(cf_coord_var.cf_name)))

    # Get any coordinate bounds.
    cf_bounds_var, climatological = get_cf_bounds_var(cf_coord_var)
    if cf_bounds_var is not None:
        bounds_data = cf_bounds_var[:]
        # Gracefully fill bounds masked array.
        if ma.is_masked(bounds_data):
            bounds_data = ma.filled(bounds_data)
            msg = "Gracefully filling {!r} dimension coordinate masked bounds"
            warnings.warn(msg.format(str(cf_coord_var.cf_name)))
        # Handle transposed bounds where the vertex dimension is not
        # the last one. Test based on shape to support different
        # dimension names.
        if cf_bounds_var.shape[:-1] != cf_coord_var.shape:
            bounds_data = reorder_bounds_data(
                bounds_data, cf_bounds_var, cf_coord_var
            )
    else:
        bounds_data = None

    # Determine whether the coordinate is circular.
    circular = False
    if (
        points_data.ndim == 1
        and coord_name in [CF_VALUE_STD_NAME_LON, CF_VALUE_STD_NAME_GRID_LON]
        and cf_units.Unit(attr_units)
        in [cf_units.Unit("radians"), cf_units.Unit("degrees")]
    ):
        modulus_value = cf_units.Unit(attr_units).modulus
        circular = iris.util._is_circular(
            points_data, modulus_value, bounds=bounds_data
        )

    # Determine the name of the dimension/s shared between the CF-netCDF data variable
    # and the coordinate being built.
    common_dims = [
        dim for dim in cf_coord_var.dimensions if dim in cf_var.dimensions
    ]
    data_dims = None
    if common_dims:
        # Calculate the offset of each common dimension.
        data_dims = [cf_var.dimensions.index(dim) for dim in common_dims]

    # Determine the standard_name, long_name and var_name
    standard_name, long_name, var_name = get_names(
        cf_coord_var, coord_name, attributes
    )

    # Create the coordinate.
    try:
        coord = iris.coords.DimCoord(
            points_data,
            standard_name=standard_name,
            long_name=long_name,
            var_name=var_name,
            units=attr_units,
            bounds=bounds_data,
            attributes=attributes,
            coord_system=coord_system,
            circular=circular,
            climatological=climatological,
        )
    except ValueError as e_msg:
        # Attempt graceful loading.
        coord = iris.coords.AuxCoord(
            points_data,
            standard_name=standard_name,
            long_name=long_name,
            var_name=var_name,
            units=attr_units,
            bounds=bounds_data,
            attributes=attributes,
            coord_system=coord_system,
            climatological=climatological,
        )
        cube.add_aux_coord(coord, data_dims)
        msg = (
            "Failed to create {name!r} dimension coordinate: {error}\n"
            "Gracefully creating {name!r} auxiliary coordinate instead."
        )
        warnings.warn(msg.format(name=str(cf_coord_var.cf_name), error=e_msg))
    else:
        # Add the dimension coordinate to the cube.
        if data_dims:
            cube.add_dim_coord(coord, data_dims)
        else:
            # Scalar coords are placed in the aux_coords container.
            cube.add_aux_coord(coord, data_dims)

    # Update the coordinate to CF-netCDF variable mapping.
    engine.cube_parts["coordinates"].append((coord, cf_coord_var.cf_name))


################################################################################
def build_auxiliary_coordinate(
    engine, cf_coord_var, coord_name=None, coord_system=None
):
    """Create an auxiliary coordinate (AuxCoord) and add it to the cube."""

    cf_var = engine.cf_var
    cube = engine.cube
    attributes = {}

    # Get units
    attr_units = get_attr_units(cf_coord_var, attributes)

    # Get any coordinate point data.
    if isinstance(cf_coord_var, cf.CFLabelVariable):
        points_data = cf_coord_var.cf_label_data(cf_var)
    else:
        points_data = _get_cf_var_data(cf_coord_var, engine.filename)

    # Get any coordinate bounds.
    cf_bounds_var, climatological = get_cf_bounds_var(cf_coord_var)
    if cf_bounds_var is not None:
        bounds_data = _get_cf_var_data(cf_bounds_var, engine.filename)

        # Handle transposed bounds where the vertex dimension is not
        # the last one. Test based on shape to support different
        # dimension names.
        if cf_bounds_var.shape[:-1] != cf_coord_var.shape:
            # Resolving the data to a numpy array (i.e. *not* masked) for
            # compatibility with array creators (i.e. dask)
            bounds_data = np.asarray(bounds_data)
            bounds_data = reorder_bounds_data(
                bounds_data, cf_bounds_var, cf_coord_var
            )
    else:
        bounds_data = None

    # Determine the name of the dimension/s shared between the CF-netCDF data variable
    # and the coordinate being built.
    common_dims = [
        dim for dim in cf_coord_var.dimensions if dim in cf_var.dimensions
    ]
    data_dims = None
    if common_dims:
        # Calculate the offset of each common dimension.
        data_dims = [cf_var.dimensions.index(dim) for dim in common_dims]

    # Determine the standard_name, long_name and var_name
    standard_name, long_name, var_name = get_names(
        cf_coord_var, coord_name, attributes
    )

    # Create the coordinate
    coord = iris.coords.AuxCoord(
        points_data,
        standard_name=standard_name,
        long_name=long_name,
        var_name=var_name,
        units=attr_units,
        bounds=bounds_data,
        attributes=attributes,
        coord_system=coord_system,
        climatological=climatological,
    )

    # Add it to the cube
    cube.add_aux_coord(coord, data_dims)

    # Make a list with names, stored on the engine, so we can find them all later.
    engine.cube_parts["coordinates"].append((coord, cf_coord_var.cf_name))


################################################################################
def build_cell_measures(engine, cf_cm_var):
    """Create a CellMeasure instance and add it to the cube."""
    cf_var = engine.cf_var
    cube = engine.cube
    attributes = {}

    # Get units
    attr_units = get_attr_units(cf_cm_var, attributes)

    # Get (lazy) content array
    data = _get_cf_var_data(cf_cm_var, engine.filename)

    # Determine the name of the dimension/s shared between the CF-netCDF data variable
    # and the coordinate being built.
    common_dims = [
        dim for dim in cf_cm_var.dimensions if dim in cf_var.dimensions
    ]
    data_dims = None
    if common_dims:
        # Calculate the offset of each common dimension.
        data_dims = [cf_var.dimensions.index(dim) for dim in common_dims]

    # Determine the standard_name, long_name and var_name
    standard_name, long_name, var_name = get_names(cf_cm_var, None, attributes)

    # Obtain the cf_measure.
    measure = cf_cm_var.cf_measure

    # Create the CellMeasure
    cell_measure = iris.coords.CellMeasure(
        data,
        standard_name=standard_name,
        long_name=long_name,
        var_name=var_name,
        units=attr_units,
        attributes=attributes,
        measure=measure,
    )

    # Add it to the cube
    cube.add_cell_measure(cell_measure, data_dims)

    # Make a list with names, stored on the engine, so we can find them all later.
    engine.cube_parts["cell_measures"].append(
        (cell_measure, cf_cm_var.cf_name)
    )


################################################################################
def build_ancil_var(engine, cf_av_var):
    """Create an AncillaryVariable instance and add it to the cube."""
    cf_var = engine.cf_var
    cube = engine.cube
    attributes = {}

    # Get units
    attr_units = get_attr_units(cf_av_var, attributes)

    # Get (lazy) content array
    data = _get_cf_var_data(cf_av_var, engine.filename)

    # Determine the name of the dimension/s shared between the CF-netCDF data variable
    # and the AV being built.
    common_dims = [
        dim for dim in cf_av_var.dimensions if dim in cf_var.dimensions
    ]
    data_dims = None
    if common_dims:
        # Calculate the offset of each common dimension.
        data_dims = [cf_var.dimensions.index(dim) for dim in common_dims]

    # Determine the standard_name, long_name and var_name
    standard_name, long_name, var_name = get_names(cf_av_var, None, attributes)

    # Create the AncillaryVariable
    av = iris.coords.AncillaryVariable(
        data,
        standard_name=standard_name,
        long_name=long_name,
        var_name=var_name,
        units=attr_units,
        attributes=attributes,
    )

    # Add it to the cube
    cube.add_ancillary_variable(av, data_dims)

    # Make a list with names, stored on the engine, so we can find them all later.
    engine.cube_parts["ancillary_variables"].append((av, cf_av_var.cf_name))


################################################################################
def _is_lat_lon(
    cf_var, ud_units, std_name, std_name_grid, axis_name, prefixes
):
    """
    Determine whether the CF coordinate variable is a latitude/longitude variable.

    Ref: [CF] Section 4.1 Latitude Coordinate.
         [CF] Section 4.2 Longitude Coordinate.

    """
    is_valid = False
    attr_units = getattr(cf_var, CF_ATTR_UNITS, None)

    if attr_units is not None:
        attr_units = attr_units.lower()
        is_valid = attr_units in ud_units

        # Special case - Check for rotated pole.
        if attr_units == "degrees":
            attr_std_name = getattr(cf_var, CF_ATTR_STD_NAME, None)
            if attr_std_name is not None:
                is_valid = attr_std_name.lower() == std_name_grid
            else:
                is_valid = False
                # TODO: check that this interpretation of axis is correct.
                attr_axis = getattr(cf_var, CF_ATTR_AXIS, None)
                if attr_axis is not None:
                    is_valid = attr_axis.lower() == axis_name
    else:
        # Alternative is to check standard_name or axis.
        attr_std_name = getattr(cf_var, CF_ATTR_STD_NAME, None)

        if attr_std_name is not None:
            attr_std_name = attr_std_name.lower()
            is_valid = attr_std_name in [std_name, std_name_grid]
            if not is_valid:
                is_valid = any(
                    [attr_std_name.startswith(prefix) for prefix in prefixes]
                )
        else:
            attr_axis = getattr(cf_var, CF_ATTR_AXIS, None)

            if attr_axis is not None:
                is_valid = attr_axis.lower() == axis_name

    return is_valid


################################################################################
def is_latitude(engine, cf_name):
    """Determine whether the CF coordinate variable is a latitude variable."""
    cf_var = engine.cf_var.cf_group[cf_name]
    return _is_lat_lon(
        cf_var,
        UD_UNITS_LAT,
        CF_VALUE_STD_NAME_LAT,
        CF_VALUE_STD_NAME_GRID_LAT,
        CF_VALUE_AXIS_Y,
        ["lat", "rlat"],
    )


################################################################################
def is_longitude(engine, cf_name):
    """Determine whether the CF coordinate variable is a longitude variable."""
    cf_var = engine.cf_var.cf_group[cf_name]
    return _is_lat_lon(
        cf_var,
        UD_UNITS_LON,
        CF_VALUE_STD_NAME_LON,
        CF_VALUE_STD_NAME_GRID_LON,
        CF_VALUE_AXIS_X,
        ["lon", "rlon"],
    )


################################################################################
def is_projection_x_coordinate(engine, cf_name):
    """
    Determine whether the CF coordinate variable is a
    projection_x_coordinate variable.

    """
    cf_var = engine.cf_var.cf_group[cf_name]
    attr_name = getattr(cf_var, CF_ATTR_STD_NAME, None) or getattr(
        cf_var, CF_ATTR_LONG_NAME, None
    )
    return attr_name == CF_VALUE_STD_NAME_PROJ_X


################################################################################
def is_projection_y_coordinate(engine, cf_name):
    """
    Determine whether the CF coordinate variable is a
    projection_y_coordinate variable.

    """
    cf_var = engine.cf_var.cf_group[cf_name]
    attr_name = getattr(cf_var, CF_ATTR_STD_NAME, None) or getattr(
        cf_var, CF_ATTR_LONG_NAME, None
    )
    return attr_name == CF_VALUE_STD_NAME_PROJ_Y


################################################################################
def is_time(engine, cf_name):
    """
    Determine whether the CF coordinate variable is a time variable.

    Ref: [CF] Section 4.4 Time Coordinate.

    """
    cf_var = engine.cf_var.cf_group[cf_name]
    attr_units = getattr(cf_var, CF_ATTR_UNITS, None)

    attr_std_name = getattr(cf_var, CF_ATTR_STD_NAME, None)
    attr_axis = getattr(cf_var, CF_ATTR_AXIS, "")
    try:
        is_time_reference = cf_units.Unit(attr_units or 1).is_time_reference()
    except ValueError:
        is_time_reference = False

    return is_time_reference and (
        attr_std_name == "time" or attr_axis.lower() == CF_VALUE_AXIS_T
    )


################################################################################
def is_time_period(engine, cf_name):
    """Determine whether the CF coordinate variable represents a time period."""
    is_valid = False
    cf_var = engine.cf_var.cf_group[cf_name]
    attr_units = getattr(cf_var, CF_ATTR_UNITS, None)

    if attr_units is not None:
        try:
            is_valid = cf_units.is_time(attr_units)
        except ValueError:
            is_valid = False

    return is_valid


################################################################################
def is_grid_mapping(engine, cf_name, grid_mapping):
    """Determine whether the CF grid mapping variable is of the appropriate type."""

    is_valid = False
    cf_var = engine.cf_var.cf_group[cf_name]
    attr_mapping_name = getattr(cf_var, CF_ATTR_GRID_MAPPING_NAME, None)

    if attr_mapping_name is not None:
        is_valid = attr_mapping_name.lower() == grid_mapping

    return is_valid


################################################################################
def _is_rotated(engine, cf_name, cf_attr_value):
    """Determine whether the CF coordinate variable is rotated."""

    is_valid = False
    cf_var = engine.cf_var.cf_group[cf_name]
    attr_std_name = getattr(cf_var, CF_ATTR_STD_NAME, None)

    if attr_std_name is not None:
        is_valid = attr_std_name.lower() == cf_attr_value
    else:
        attr_units = getattr(cf_var, CF_ATTR_UNITS, None)
        if attr_units is not None:
            is_valid = attr_units.lower() == "degrees"

    return is_valid


################################################################################
def is_rotated_latitude(engine, cf_name):
    """Determine whether the CF coodinate variable is rotated latitude."""
    return _is_rotated(engine, cf_name, CF_VALUE_STD_NAME_GRID_LAT)


###############################################################################
def is_rotated_longitude(engine, cf_name):
    """Determine whether the CF coordinate variable is rotated longitude."""
    return _is_rotated(engine, cf_name, CF_VALUE_STD_NAME_GRID_LON)


################################################################################
def has_supported_mercator_parameters(engine, cf_name):
    """Determine whether the CF grid mapping variable has the supported
    values for the parameters of the Mercator projection."""

    is_valid = True
    cf_grid_var = engine.cf_var.cf_group[cf_name]

    false_easting = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_EASTING, None)
    false_northing = getattr(cf_grid_var, CF_ATTR_GRID_FALSE_NORTHING, None)
    scale_factor_at_projection_origin = getattr(
        cf_grid_var, CF_ATTR_GRID_SCALE_FACTOR_AT_PROJ_ORIGIN, None
    )
    standard_parallel = getattr(
        cf_grid_var, CF_ATTR_GRID_STANDARD_PARALLEL, None
    )

    if false_easting is not None and false_easting != 0:
        warnings.warn(
            "False eastings other than 0.0 not yet supported "
            "for Mercator projections"
        )
        is_valid = False
    if false_northing is not None and false_northing != 0:
        warnings.warn(
            "False northings other than 0.0 not yet supported "
            "for Mercator projections"
        )
        is_valid = False
    if (
        scale_factor_at_projection_origin is not None
        and scale_factor_at_projection_origin != 1
    ):
        warnings.warn(
            "Scale factors other than 1.0 not yet supported for "
            "Mercator projections"
        )
        is_valid = False
    if standard_parallel is not None and standard_parallel != 0:
        warnings.warn(
            "Standard parallels other than 0.0 not yet "
            "supported for Mercator projections"
        )
        is_valid = False

    return is_valid


################################################################################
def has_supported_stereographic_parameters(engine, cf_name):
    """Determine whether the CF grid mapping variable has a value of 1.0
    for the scale_factor_at_projection_origin attribute."""

    is_valid = True
    cf_grid_var = engine.cf_var.cf_group[cf_name]

    scale_factor_at_projection_origin = getattr(
        cf_grid_var, CF_ATTR_GRID_SCALE_FACTOR_AT_PROJ_ORIGIN, None
    )

    if (
        scale_factor_at_projection_origin is not None
        and scale_factor_at_projection_origin != 1
    ):
        warnings.warn(
            "Scale factors other than 1.0 not yet supported for "
            "stereographic projections"
        )
        is_valid = False

    return is_valid
