import time
time.sleep(5)

# regex
import re

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# used before
import requests
from selenium.webdriver.edge.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import csv
csv_file_name = "course_titles.csv"

# path to local edge driver
edge_driver_path = 'C:\\Users\\ZSY\\OneDrive\\桌面\\college\\23Fall\\MAD2502 Intro to Computational Math\\Capstone\\scraping\\msedgedriver.exe'
service = Service(edge_driver_path)

driver = webdriver.Edge(service=service)

def find_sibling_div_by_label(session, label):
    # for class without unique names
    span = session.find('span', string=lambda x: x and label in x)
    return span.find_next('div').get_text(strip=True) if span else None

def get_meeting_times_and_location(session):
    # Check for the 'To Arrange' button within the session
    to_arrange = session.find(string="To Arrange")
    if to_arrange:
        return "To Arrange", "To Arrange"

    # If there's no 'To Arrange' button, proceed to find times and locations
    times = session.find_all("div", class_="sc-fIGJwM fCxjwG")
    locations = session.find_all("a", class_="sc-dAbbOL inthLk MuiTypography-root MuiTypography-body1 sc-dBmzty kGZliN MuiLink-root MuiLink-underlineNone")

    meeting_times = ' & '.join(' '.join(part.get_text(strip=True) for part in time.find_all("div", class_="sc-jkTpcO fCUEaT")) for time in times)
    # Clean up the meeting time string
    meeting_times = re.sub(r'\s*\blaunch\b', '', meeting_times).strip()
    meeting_times = re.sub(r'[\xa0\u202f\u00a0]', ' ', meeting_times)

    # Combine location texts, and clean up as needed
    location_texts = ' & '.join(location.get_text(strip=True) for location in locations)
    location_texts = re.sub(r'\s*\blaunch\b', '', location_texts).strip()
    location_texts = re.sub(r'[\xa0\u202f\u00a0]', ' ', location_texts)

    return meeting_times, location_texts


# adjust url for different specifications or terms
# this one only reads the undergraduate courses
url = "https://one.uf.edu/soc/?category=%22CWSP%22&term=%222241%22&prog-level=%22UGRD%22"
driver.get(url)



try:
    while True:  # run until reached to the end
        # Wait for the "View More Results" button to become clickable
        view_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[text()="View More Results"]'))
        )
        # Click the button
        view_more_button.click()

except: # (NoSuchElementException, TimeoutException) avoid timeout error when reached the bottom
    print("All results loaded or button not found.")

finally:
        # Parse the content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')

       # Initialize a list to store course information
    course_info = []

        # Iterate through each course container
    for course in soup.find_all("div", class_="accordion__container"):
        # Extract the course title
        title_section = course.find("p", class_="sc-dAbbOL fRppTZ MuiTypography-root MuiTypography-body1 sc-lgjHQU fkPCVF")
        course_title = title_section.text.strip() if title_section else "NA"


        for session in course.find_all("div", class_ = "sc-cPiKLX fDvufK MuiPaper-root MuiPaper-outlined MuiPaper-rounded sc-fLvQuD PELBi"):
            class_section = session.find("div", class_ = "sc-huFNyZ ihbfhu")
            class_digit = class_section.text.strip() if class_section else "NA"

            # Extract the instructor name
            instructor_section = session.find("p", class_="sc-dAbbOL fRppTZ MuiTypography-root MuiTypography-body1 sc-dISpDn iKiLsw")
            instructor = instructor_section.text.strip() if instructor_section else "NA"

            meet_section = session.find("div", class_="sc-iLWXdy gXCWMz")
            meet = meet_section.text.strip() if meet_section else "NA"

            credits_info = find_sibling_div_by_label(course, "Credits")
            department_info = find_sibling_div_by_label(course, "Department")
            final_exam_info = find_sibling_div_by_label(course, "Final Exam")
            class_dates_info = find_sibling_div_by_label(course, "Class Dates")

            meeting_time, location = get_meeting_times_and_location(session)

            # no meeting time info and is Online mean that the class is asynchronous
            if "Online" in meet and not meeting_time:
                meeting_time, location = "asynchronous", "asynchronous"
            # only no location and is Online mean that the class is remote
            if "Online" in meet and not location:
                location = "remote"

            # Append the extracted information to the course_info list
            course_info.append([course_title, class_digit, instructor,
                                credits_info, department_info, final_exam_info,
                                class_dates_info, meeting_time, location,
                                meet])

    with open(csv_file_name, 'w', newline='', encoding='utf-8') as file:
    # Create a CSV writer object
        writer = csv.writer(file)

    # Write a header row
        writer.writerow(['Course Title', "Class Digit", 'Instructor',
                         "Credit", "Department", "Final Exam Date",
                         "Class Date Info", "Meeting Time", "Location",
                         "Meet"])

    # Write the course info to the CSV file
        for title, class_digit, instructor, credit, department, final, date, meet_time, location, meet_info in course_info:
            writer.writerow([title, class_digit, instructor, credit, department, final, date, meet_time, location, meet_info])

    driver.quit()

