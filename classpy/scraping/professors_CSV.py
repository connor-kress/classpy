import pandas as pd
import csv

# threading to increase scraping speed
from concurrent.futures import ThreadPoolExecutor
import concurrent

from .ratemyprof_scrape import search_professor
from ..data.raw_data import (
    EDGE_DRIVER_PATH,
    COURSE_TITLES_PATH,
    PROFESSORS_PATH,
)


def scrape_professor_data() -> None:
    # read professor name
    course_data = pd.read_csv(COURSE_TITLES_PATH)

    # convert to list
    professor_names = course_data["Instructor"].unique().tolist()

    fieldnames = ['Instructor', 'Department', 'University', 'rating_value',
                  'num_ratings', 'would_take_again', 'level_of_difficulty']
    i = 1
    def scrape_professor(professor):
        prof_list = search_professor(professor, EDGE_DRIVER_PATH)
        if prof_list is None:
            prof_list = [{field: (professor if field == 'Instructor'
                                  else 'University of Florida'
                                  if field == 'University' else 'None')
                                  for field in fieldnames}]
        return prof_list

    with ThreadPoolExecutor(max_workers=25) as executor:
        # Submitting tasks for each professor
        future_to_professor = {executor.submit(scrape_professor, prof): prof
                               for prof in professor_names}

        # writing the header row
        with open(PROFESSORS_PATH, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            # collecting and writing results as they are completed
            for future in concurrent.futures.as_completed(future_to_professor):
                print(i)
                i += 1

                professor = future_to_professor[future]
                try:
                    prof_list = future.result()
                    writer.writerows(prof_list)
                except Exception as e:
                    print(f"Error fetching data for {professor}: {e}")
