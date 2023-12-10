import os

__ROOT = os.path.dirname(__file__)

BUS_STOPS_PATH = os.path.join(__ROOT, 'bus_stops.json')
BUILDINGS_PATH = os.path.join(__ROOT, 'buildings.json')

COURSE_TITLES_PATH = os.path.join(__ROOT, 'course_titles.csv')
COURSE_WITH_SCORE_PATH = os.path.join(__ROOT, 'course_with_score.csv')
PROFESSORS_PATH = os.path.join(__ROOT, 'professors.csv')
PROFESSORS_CLEANED_PATH = os.path.join(__ROOT, 'professors_cleaned.csv')

SS_PATH = os.path.join(__ROOT, '..', 'images')
SS_PATH = os.path.normpath(SS_PATH) + os.sep
