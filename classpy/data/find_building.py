from .locations import BUILDINGS
from ..locations import Building


def get_building(abbrev: str) -> Building:
    try:
        return next(bldg for bldg in BUILDINGS if bldg.abbrev == abbrev)
    except StopIteration:
        raise Exception(f'"{abbrev}" could not be found.')
