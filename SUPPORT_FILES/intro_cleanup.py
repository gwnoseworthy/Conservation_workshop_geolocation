# -*- coding: ascii -*-
"""
Pull nl placenames from canada gedcodes
"""
__author__ = 'Gerard Noseworthy - Integrated Informatics Inc.'

# CONSTANTS
COMMA = ','
SPACE = ' '
TAB_SYMBOL = '\t'
# LOCATION OF INITIAL DATASET FROM GEONAMES.ORG
# NOTE: The 'r' before the string means to interpret it raw, this ignores
# NOTE: slashes as topographic symbols
PLACENAME_SOURCE = r'/Users/gwnoseworthy/Demos/CIG_Workshop/CA.txt'
# MY OUTPUT LOCATION
OUTPUT_SOURCE = r'/Users/gwnoseworthy/Demos/CIG_Workshop/COORDS.csv'


# FIELD INDEXES FROM README.TXT
PROVINCE_CODE_INDEX = 10
PLACE_NAME_INDEX = 1
PLACE_ALT_INDEX = 2
LAT_INDEX = 4
LONG_INDEX = 5
OUTPUT_ENTRY = [PLACE_NAME_INDEX, PLACE_ALT_INDEX, LAT_INDEX, LONG_INDEX]

# PROVINCE CODE FROM REVIEW OF THE DATASET
NL_PROVINCE_CODE = '05'

# CREATE A SPOT TO KEEP OUR RESULTS IN MEMORTY
results = []

# OPEN FILE FOR READING
with open(PLACENAME_SOURCE) as place_file:
    for row in place_file:
        # THE DATA IS FORMATED TO BE TAB DELIMITED SO WE CAN SPLIT BY \t
        # (which is the typographic representation for tab)
        split_row = row.split(TAB_SYMBOL)

        # GRAB OUR LAT/LONG FOR EACH ENTRY
        lat = split_row[LAT_INDEX]
        lon = split_row[LONG_INDEX]
        # WE ONLY WANT ENTRIES FROM NL
        province_code = split_row[PROVINCE_CODE_INDEX]
        if province_code == NL_PROVINCE_CODE:
            place_name = split_row[PLACE_NAME_INDEX]
            place_name = place_name.replace(COMMA, SPACE)
            alternate_names = split_row[PLACE_ALT_INDEX]
            # WE KNOW THAT ALTERNATE NAMES A COMMA DELIMITED SO CHECK FOR MULTIPLE NAMES
            if COMMA in alternate_names:
                names = alternate_names.split(COMMA)
                #ADD original name to alternates
                names.append(place_name)
            else:
                # IF THERE IS NO COMMA THEN JUST USE THE REGULAR AND ALT ANMES
                names = [alternate_names, place_name]
            # WE WILL USE A SET THAT AUTOMATICALL WILL REMOVE IDENTICAL NAMES
            placenames = set(names)
            # AND ADD ALL OUR RESULTS FOR THE ENTRY
            for name in placenames:
                record = [name, lon, lat]
                results.append(record)
# NOW OPEN A FILE TO WRITE THE 'w' ARGUEMENT MEANS WRITE MODE
with open(OUTPUT_SOURCE, 'w') as out_file:
    output_placeholder = '{0},{1},{2}\n'
    # WRITE A HEADER ROW:
    out_file.write(output_placeholder.format('PLACE', 'LONG', 'LAT'))
    # LOOPING OVER OUR RESULTS
    for res in results:
        # ASSIGN ALL 3 values to variables
        place, lon, lat = res
        out_file.write(output_placeholder.format(place, lon, lat))






