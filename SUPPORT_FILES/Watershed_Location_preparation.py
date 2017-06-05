# -*- coding: ascii -*-
"""
Reduce water supply data to best possible outcome for use in tutorial
"""
from csv import DictReader

OUTPUT_SOURCE = r'/Users/gwnoseworthy/Demos/CIG_Workshop/COORDS.csv'
WS_LOCATIONS = r'/Users/gwnoseworthy/Demos/CIG_Workshop/TutorialWaterSupplies.csv'
WATER_SOURCE = r'/Users/gwnoseworthy/Demos/CIG_Workshop/PublicWaterSupplies.csv'

COMMA = ','
SPACE = ' '
APOS = "'"
PIPE = '|'
HYPHEN = '-'





def output_record(args):
    """
    return formatted record
    """
    return COMMA.join(args) + '\n'
# End output_records function


def find_match(source_string, geolocations):
    """
    Attempt to match to the best field ot find geolocation matches
    """
    if not source_string:
        return None, 0,0,0, ''
    missing, exact, vague = 0,0,0
    best_match = ''
    ws_location = None
    for char in (HYPHEN, COMMA):
        source_string = source_string.replace(char, '')
    for attempt in source_string.split(PIPE):
        attempt = attempt.strip()
        if not attempt:
            continue
        ws_location = geolocations.get(attempt)
        if not ws_location and APOS in attempt:
            attempt = attempt.replace(APOS, '')
            ws_location = geolocations.get(attempt)
        if ws_location:
            best_match = attempt
            break

    if not ws_location:
        missing = 0

    elif len(ws_location) == 1:
        exact = 1

    else:
        count = len(ws_location)
        if count > 10:
            vague = 1
    return ws_location, vague, missing, exact, best_match
# End find_match function


def coords_lookup():
    """
    create geolocations lookup
    """
    geolocations = dict()
    with open(OUTPUT_SOURCE) as coords:
        for row in coords:
            row = row.replace('\n', '')
            split_row = row.split(',')
            place, lon, lat = split_row
            coordinates = lon, lat
            if place in geolocations:
                geolocations[place].append(coordinates)
            else:
                geolocations[place] = [coordinates]
    return geolocations
# End coords_lookup function


def match_to_coords():
    """
    Match entries to known names
    """
    water_info = []
    missing_count = 0
    exact_count = 0
    vague_count = 0

    geolocations = coords_lookup()
    with open(WATER_SOURCE) as pws_file:
        reader = DictReader(pws_file)
        for record in reader:
            source = record.get('SOURCENAME').replace(COMMA, '')
            community = record.get('COMMUNITY').replace(COMMA, '')
            area = record.get('AREASERVED').replace(COMMA, '')
            supply_type = record.get('SUPPLYTYPE')
            status = record.get('PROTECTED')
            ws_location, vague, missing, exact, best_match = find_match(
                source, geolocations)
            ws_location = ws_location or []
            if not exact:
                area = area.replace('Area', '').replace('area', '')

                area_match, vague, missing, exact, best_area = find_match(
                    area, geolocations)
                if area_match and len(area_match) >= len(ws_location):
                    ws_location = area_match
                    best_match = best_area
            if not exact:
                community_match, vague, missing, exact, best_com = find_match(
                    community, geolocations)

                if community_match and len(ws_location) < community_match:
                    ws_location = community_match
                    best_match = best_com
            exact_count += exact
            vague_count += vague
            missing_count += missing

            if vague:
                print source, '||', area

            if not ws_location:
                print source, '||', area
                continue
            atts = (best_match, community, area, source, supply_type, status)
            water_info.append(output_record(atts))

    with open(WS_LOCATIONS, 'w') as output_file:
        header = ('BEST_MATCH', 'COMMUNITY',
                  'AREA', 'SOURCE', 'SUPPLY_TYPE', 'STATUS')
        output_file.write(output_record(header))
        output_file.writelines(water_info)

    print vague_count
    print missing_count
    print exact_count


if __name__ == '__main__':
    match_to_coords()
