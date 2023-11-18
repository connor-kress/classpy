from typing import Optional

from ..utils import haversine
from .coordinates import Coords

def distance(__P0: Coords, __P1: Coords) -> float:
    """Calculates the distance between two coordinate locations."""
    lat0, lon0 = __P0.lat, __P0.lon
    lat1, lon1 = __P1.lat, __P1.lon
    return haversine(lat0, lon0, lat1, lon1)
