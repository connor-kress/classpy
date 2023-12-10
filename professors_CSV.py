import ratemyprof_scrape as rp
import pandas as pd
import csv

# threading to increase scraping speed
from concurrent.futures import ThreadPoolExecutor
import concurrent

# to local driver
edge_driver_path = 'C:\\Users\\ZSY\\OneDrive\\桌面\\college\\23Fall\\MAD2502 Intro to Computational Math\\classpy\\scrape\\msedgedriver.exe'


# read professor name
file_path = "course_titles.csv"
course_data = pd.read_csv(file_path)

# convert to list
professor_names = course_data["Instructor"].unique().tolist()

filename = "professors.csv"
fieldnames = ['Instructor', 'Department', 'University', 'rating_value', 'num_ratings', 'would_take_again',
              'level_of_difficulty']
i = 1
def scrape_professor(professor):
    prof_list = rp.search_professor(professor, edge_driver_path)
    if prof_list is None:
        prof_list = [{field: (professor if field == 'Instructor' else 'University of Florida' if field == 'University' else 'None') for field in fieldnames}]
    return prof_list

with ThreadPoolExecutor(max_workers=25) as executor:
    # Submitting tasks for each professor
    future_to_professor = {executor.submit(scrape_professor, professor): professor for professor in professor_names}

    # writing the header row
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        # collecting and writing results as they are completed
        for future in concurrent.futures.as_completed(future_to_professor):
            print(f"{i}")
            i = i + 1

            professor = future_to_professor[future]
            try:
                prof_list = future.result()
                for prof_dict in prof_list:
                    writer.writerow(prof_dict)
            except Exception as e:
                print(f"Error fetching data for {professor}: {e}")
