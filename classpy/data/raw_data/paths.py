import os

__ROOT = os.path.dirname(__file__)

BUS_STOPS_PATH = os.path.join(__ROOT, 'bus_stops.json')
BUILDINGS_PATH = os.path.join(__ROOT, 'buildings.json')

SS_PATH = os.path.join(__ROOT, '..', 'images')
SS_PATH = os.path.normpath(SS_PATH) + os.sep
