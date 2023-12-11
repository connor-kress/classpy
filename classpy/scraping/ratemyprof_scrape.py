import requests
import os
from bs4 import BeautifulSoup
from typing import Optional

# dynamically loaded, use selenium
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options


def search_professor(
    name: str,
    driver_path: os.PathLike,
) -> Optional[list[dict[str, str]]]:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')  # needed for Windows

    url = "https://www.ratemyprofessors.com/search/professors/1100"
    prof_url = "https://www.ratemyprofessors.com/professor/"

    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=options)

    encoded_name = requests.utils.quote(name)
    search_url = f"{url}?q={encoded_name}"
    driver.get(search_url)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    # halt if no prof found at this name
    no_results_name = soup.find('div', class_='NoResultsFoundArea__NoResultsFoundHeader-mju9e6-1')
    no_results_uf = soup.find(string="No professors with ")
    if no_results_name or no_results_uf:
        return None

    professors_data = []
    # the outer site is not uptodate, extract prof id to scrape each prof site
    for TeacherCard in soup.find_all("a", class_="TeacherCard__StyledTeacherCard-syjs0d-0"):
        # href attribute for id
        href_value = TeacherCard['href']
        # extract professor id
        professor_id = href_value.split('/')[-1]

        professor_url = f"{prof_url}{professor_id}"
        driver.get(professor_url)
        professor_site = BeautifulSoup(driver.page_source, "html.parser")

        prof_rating_element = professor_site.find('div', class_='RatingValue__Numerator-qw8sqy-2 liyUjw')
        prof_rating = prof_rating_element.get_text() if prof_rating_element else "NA"

        prof_name_element = professor_site.find('div', class_='NameTitle__Name-dowf0z-0 cfjPUG')
        prof_name = prof_name_element.get_text() if prof_name_element else "NA"

        num_rating_element = professor_site.find('a', href="#ratingsList")
        num_rating = num_rating_element.get_text() if num_rating_element else "NA"
        num_rating = ''.join(filter(str.isdigit, num_rating)) # filter non-numeric
        if len(num_rating) == 0: # no rating exist
            num_rating = 0

        would_take_again = "NA"
        level_of_difficulty = "NA"

        # Find and extract 'Would take again' data
        would_take_again_element = professor_site.find('div', class_='FeedbackItem__FeedbackDescription-uof32n-2',
                                                       text='Would take again')
        if would_take_again_element:
            would_take_again_number = would_take_again_element.find_previous_sibling()
            if would_take_again_number:
                would_take_again = would_take_again_number.get_text()

        # Find and extract 'Level of Difficulty' data
        level_of_difficulty_element = professor_site.find('div', class_='FeedbackItem__FeedbackDescription-uof32n-2',
                                                          text='Level of Difficulty')
        if level_of_difficulty_element:
            level_of_difficulty_number = level_of_difficulty_element.find_previous_sibling()
            if level_of_difficulty_number:
                level_of_difficulty = level_of_difficulty_number.get_text()


        department_element = professor_site.find('a', class_='TeacherDepartment__StyledDepartmentLink-fl79e8-0 iMmVHb')
        department = department_element.get_text() if department_element else "NA"

        university_element = professor_site.find('a', href="/school/1100")
        university = university_element.get_text() if university_element else "NA"

        # update for each prof
        professor_info = {
            'Instructor': prof_name,
            'Department': department,
            'University': university,
            'rating_value': prof_rating,
            'num_ratings': num_rating,
            'would_take_again': would_take_again,
            'level_of_difficulty': level_of_difficulty,
        }

        professors_data.append(professor_info)
    
    driver.close()
    return professors_data
