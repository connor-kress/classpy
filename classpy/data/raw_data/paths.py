import os

__ROOT = os.path.dirname(__file__)

BUS_STOPS_PATH = os.path.join(__ROOT, 'bus_stops.json')
BUILDINGS_PATH = os.path.join(__ROOT, 'buildings.json')
COURSE_TITLES_PATH = os.path.join(__ROOT, 'course_titles.csv')

SS_PATH = os.path.join(__ROOT, '..', 'images')
SS_PATH = os.path.normpath(SS_PATH) + os.sep
