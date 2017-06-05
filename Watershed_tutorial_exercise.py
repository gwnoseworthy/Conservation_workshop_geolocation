# -*- coding: ascii -*-
"""
Geolocate Data for Watersheds
"""
# IMPORT STATEMENT
from csv import DictReader

# DEFINE PROJECT WORKSPACES
# NOTE: The 'r' before the string means to interpret it raw, this ignores
# NOTE: slashes as topographic symbols
COORD_SOURCE = r''
WS_SOURCE = r''
OUTPUT_LOCATION = r''

# DEFINE CONSTANT VALUES
COMMA = ','
BLANK = ''
# NOTE the {n} is a defined python character placeholders that are
# NOTE populated using the .format method
OUTPUT_TEMPLATE = '{0},{1},{2},{3},{4}\n'
HEADER = OUTPUT_TEMPLATE.format(
    'LON', 'LAT', 'SUPPLY_NAME', 'STATUS', 'LOCATION_COUNT')


