from typing import Optional

from .locations import BUILDINGS
from ..locations import Building


def get_building(abbrev: str) -> Optional[Building]:
    return next((bldg for bldg in BUILDINGS if bldg.abbrev == abbrev), None)
