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

geolocations = dict()  # Create an empty Dictionary to hold our coordinates
with open(COORD_SOURCE) as coord_file:  # open the file
    for row in coord_file:  # we are going to loop over the rows in the csv
        row = row.replace('\n', '')  # clean up the text by removing newline(\n)
        split_row = row.split(COMMA)  # split the csv line by commas)
        place, lon, lat = split_row  # create variables for the 3 columns
        coordinates = lon, lat  # assign the lat long to a single coord
        # NOTE: where place names are not unique we need to account for multiple
        # NOTE: place name results
        if place in geolocations:  # check to see if we got an existing result
            geolocations[place].append(coordinates)  # add the result
        else:  # if the first check fails this executes
            geolocations[place] = [coordinates]  # create a new result

water_locations = []  # Create an empty List to hold our location results
with open(WS_SOURCE) as pws_file:  # Open the Public water supply file
    # NOTE: a DictReader is part of the built in csv library that was
    # NOTE: imported earlier, that allows you to access row data by column name
    reader = DictReader(pws_file)  # transform the file into a DictReader
    for record in reader:  # Loop through the records
        # We will lookup the record by columns here, cleaning up the comma from
        # best match
        place_name = record.get('BEST_MATCH').replace(COMMA, BLANK)
        status = record.get('STATUS')  # Look up status
        locations = geolocations.get(place_name)  # Try to get the
        # Coordinates of the location from our geolocation dictionary
        if not locations:  # the get keyword is a Null if we don't have an entry
            continue  # if we don't have an entry, skip to the next water supply
        number_of_coords = len(locations)  # count the number of results to find
        # out the level of certainty we have to the location
        for location in locations:  # loop through all the dictionary results
            lon, lat = location  # get long and lat from the location
            # NOTE: This could be on one line, but you can break lines with
            # NOTE: Parentheses without changing code exectution
            output_row = OUTPUT_TEMPLATE.format(
                lon, lat, place_name, status, number_of_coords)
            # Populate the output row template
            water_locations.append(output_row)  # add our results to our list



# NOTE: we are using the 'w' argument on our outfile, this indicates we are in
# NOTE: 'w'rite Mode, with no argument it defaults to 'r'eadmode
with open(OUTPUT_LOCATION, 'w') as out_file:  # Open our output file
    out_file.write(HEADER)  # write our file header
    out_file.writelines(water_locations)  # write all our results at once

