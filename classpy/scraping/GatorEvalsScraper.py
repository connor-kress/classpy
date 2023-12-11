# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
from webdriver_manager.chrome import ChromeDriverManager
import pyautogui
import re
import os
from PIL import Image

# Initialize the Selenium Chrome Driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# Navigate to the Gator Evals Tableau page
driver.get('https://public.tableau.com/views/GatorEvalsSpring2023ThreeYears/Dashboard1?%3Adisplay_static_image=y&%3AbootstrapWhenNotified=true&%3Aembed=true&%3Alanguage=en-US&:embed=y&:showVizHome=n&:apiID=host0#navType=0&navSrc=Parse')

# Wait for the dropdown to be clickable and click it
dropdown = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.ID, 'tabZoneId12'))
)
dropdown.click()

#Function to remove punctuation and whitespace from teacher's names so they are acceptable as file names
def sanitize_filename(filename):
    # Replace spaces with underscores and remove invalid characters
    sanitized = re.sub(r'[\\/*?:"<>|,]', "", filename)
    sanitized = sanitized.replace(' ', '_')
    return sanitized

# Select each teacher in drop down menu one by one and take a screenshot
for x in range(1, 5224):
    
    # Move mouse to hover over drop down menu scroller
    pyautogui.moveTo(x=990, y=425)
    
    # Drag scroller to bottom of drop down menu to load all teacher options
    pyautogui.dragRel(xOffset=0, yOffset=570, button='PRIMARY', duration=3.0)
    
    # Select teacher
    options = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, f'FI_sqlproxy.04pjtia0xer5jm1ctta0u0ec5l1n,none:INSTRUCTOR_NAME:nk16126187992227925297_15952188591581136529_{x}'))
    )
    options.click()
    
    # Find teacher's name in html
    element = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.ID, f'FI_sqlproxy.04pjtia0xer5jm1ctta0u0ec5l1n,none:INSTRUCTOR_NAME:nk16126187992227925297_15952188591581136529_{x}'))
    )
    
    # Remove spaces and punctuation so it can be made into a file name
    element_text = element.text.strip()  # or element.text.strip()
    sanitized_text = sanitize_filename(element_text)
    
    #Save screenshot to a folder on desktop with file named after each teacher
    filename = f'C:\\Users\\aiden\\OneDrive\\Desktop\\python project\\{sanitized_text}.png'
    driver.save_screenshot(filename)

    # Wait for the dropdown to be clickable again and click it
    dropdown = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, 'tabZoneId12'))
    )
    dropdown.click()

    # Short delay so drop down menu has enough time to open
    time.sleep(1)
    

# Close the driver when done
driver.quit()

#Images show the entire gatorevals screen so they need to be cropped to focus on the chart
def crop_images_in_folder(source_folder, dest_folder, crop_coordinates):
   
    # Create the destination folder if it does not exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Get a list of files in the source folder
    for file_name in os.listdir(source_folder):
        # Construct the full file path
        file_path = os.path.join(source_folder, file_name)
        
        # Check if it's a file and not a directory and has an image extension
        if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            # Open the image
            with Image.open(file_path) as img:
                # Crop the image using the provided coordinates
                cropped_img = img.crop(crop_coordinates)
                
                # Construct the full path for the destination of the cropped image
                dest_file_path = os.path.join(dest_folder, file_name)
                
                # Save the cropped image
                cropped_img.save(dest_file_path)
                print(f"Cropped image saved as {dest_file_path}")

# Define the source and destination folders
source_folder = 'C:\\Users\\aiden\\OneDrive\\Desktop\\python project'
dest_folder = 'C:\\Users\\aiden\\OneDrive\\Desktop\\python project'

# Define your crop coordinates (left, upper, right, lower)
crop_coordinates = (0, 0, 1000, 825)

# Call the function to crop the images
crop_images_in_folder(source_folder, dest_folder, crop_coordinates)

# Compresses folder from around 500mb to 350mb
# The setting for quality, set to 60 here, can be lowered or raised if needed
def compress_images_in_folder(source_folder, dest_folder, quality=60):
    
    # Create the destination folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # List all files in the source folder
    files = os.listdir(source_folder)

    # Loop over all files in the directory
    for file_name in files:
        # Construct full file path
        file_path = os.path.join(source_folder, file_name)
        
        # Check if the file is an image
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            with Image.open(file_path) as img:
                # Convert the image to RGB mode (this step is necessary for .png files to be saved as .jpeg)
                if img.mode in ("RGBA", "P"):
                    img = img.convert("RGB")

                # Construct the full path for the destination of the compressed image
                dest_file_path = os.path.join(dest_folder, file_name)
                
                # Save the image with the desired compression
                img.save(dest_file_path, quality=quality, optimize=True)
                print(f"Compressed image saved to {dest_file_path}")

# Define your source and destination folders
source_folder = 'C:\\Users\\aiden\\OneDrive\\Desktop\\python project'
dest_folder = 'C:\\Users\\aiden\\OneDrive\\Desktop\\python project'

# Call the function to compress the images
compress_images_in_folder(source_folder, dest_folder, quality=60)



