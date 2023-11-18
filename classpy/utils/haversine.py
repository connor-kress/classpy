from math import radians, asin, sin, cos, sqrt

EARTH_RADIUS_KM = 6378


def haversine(lat0: float, lon0: float, lat1: float, lon1: float) -> float:
    """Calculates the great circle distance between two points on the earth
    (decimal degrees -> kilometers).
    """
    # convert decimal degrees to radians 
    lat0, lon0, lat1, lon1 = map(radians, (lat0, lon0, lat1, lon1))

    # haversine formula
    dlat = lat1 - lat0
    dlon = lon1 - lon0
    a = sin(dlat/2)**2 + cos(lat0)*cos(lat1)*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return c * EARTH_RADIUS_KM
