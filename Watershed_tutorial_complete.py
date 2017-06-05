# -*- coding: ascii -*-
"""
Geolocate Data for Watersheds
"""

from csv import DictReader

# DEFINE PROJECT WORKSPACES
# NOTE: The 'r' before the string means to interpret it raw, this ignores
# NOTE: slashes as topographic symbols
COORD_SOURCE = r'/Users/gwnoseworthy/Demos/CIG_Workshop/COORDS.csv'
WS_SOURCE = r'/Users/gwnoseworthy/Demos/CIG_Workshop/TutorialWaterSupplies.csv'
OUTPUT_LOCATION = r'/Users/gwnoseworthy/Demos/CIG_Workshop/LocatedOutput.csv'

# DEFINE CONSTANT VALUES
COMMA = ','
BLANK = ''
OUTPUT_TEMPLATE = '{0},{1},{2},{3},{4}\n'

HEADER = OUTPUT_TEMPLATE.format(
    'LON', 'LAT', 'SUPPLY_NAME', 'STATUS', 'LOCATION_COUNT')

geolocations = dict()
with open(COORD_SOURCE) as coord_file:
    for row in coord_file:
        row = row.replace('\n', '')
        split_row = row.split(COMMA)
        place, lon, lat = split_row
        coordinates = lon, lat
        # NOTE: where place names are not unique we need to account for multiple
        # NOTE: place name results
        if place in geolocations:
            geolocations[place].append(coordinates)
        else:
            geolocations[place] = [coordinates]

water_locations = []
with open(WS_SOURCE) as pws_file:
    # NOTE: a DictReader is part of the built in csv library that was
    # NOTE: imported earlier, that allows you to access row data by column name
    reader = DictReader(pws_file)
    for record in reader:
        place_name = record.get('BEST_MATCH').replace(COMMA, BLANK)
        status = record.get('STATUS')
        locations = geolocations.get(place_name)

        if not locations:
            continue
        number_of_coords = len(locations)
        for location in locations:
            lon, lat = location
            # NOTE: This could be on one line, but you can break lines with
            # NOTE: Parentheses without changing code exectution
            output_row = OUTPUT_TEMPLATE.format(
                lon, lat, place_name, status, number_of_coords)
            water_locations.append(output_row)



# NOTE: we are using the 'w' argument on our outfile, this indicates we are in
# NOTE: 'w'rite Mode, with no argument it defaults to 'r'eadmode
with open(OUTPUT_LOCATION, 'w') as out_file:  # Open our output file
    out_file.write(HEADER)  # write our file header
    out_file.writelines(water_locations)  # write all our results at once

