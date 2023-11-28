import json

from ..locations import Building, Coords
from .raw_data import BUILDINGS_PATH

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
    __data_set = json.loads(file.read())

BUILDINGS = [_parse_building(data) for data in __data_set if data['JTYPE'] == 'BLDG']
# PARKS = [_parse_park?(data) for data in __data_set if data['JTYPE'] == 'PARK']
