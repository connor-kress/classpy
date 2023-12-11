��#   c l a s s p y 
 
 








# How to use GatorEvalsScraper.py and gator_evals_searcher.py

# GatorEvalsScraper.py requires selenium chromedriver and the tableau link of the Gator Evals page
# GatorEvalsScraper.py works by first simulating a user inputted click on the instructor_name dropdown menu
# pyautogui is then used to simulate a click and drag on the scrollbar of the dropdown menu
# It then uses selenium webdriver to iterate through each teacher and take a screenshot
# This screenshot is then renamed to the professor's name and croppped + compressed to focus the data
# This produces a folder to be used with the gator_evals_searcher.py 

# gator_evals_searcher.py works by first accepting a user inputted instructor name
# It then searches through the folder provided by GatorEvalsScraper.py for a filename matching that user inputted name
# If the file is found, that file is selected and shown, if not, a string is returned reporting that no image was found
