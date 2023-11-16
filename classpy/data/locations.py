import json
import os

from ..locations import Building, Coords

ROOT = os.path.dirname(__file__)
BUILDINGS_PATH = os.path.join(ROOT, '../data/buildings.json')
BUS_STOPS_PATH = os.path.join(ROOT, '../data/bus_stops.json')

type BuildingDict = dict[str, str | float]


def _parse_building(data: BuildingDict) -> Building:
    return Building(
        id=data['ID'],
        name=data['NAME'],
        common_name=data['COMMON_NAME'] or None,
        abbrev=data['ABBREV'] or None,
        coords=Coords(data['LAT'], data['LON']),
    )


with open(BUILDINGS_PATH, 'r') as file:
    data_set = json.loads(file.read())

BUILDINGS = [_parse_building(data) for data in data_set if data['JTYPE'] == 'BLDG']
# PARKS = [_parse_building(data) for data in data_set if data['JTYPE'] == 'PARK']
