import time
import re
import os
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image

from ..data.raw_data import (
    GATOR_EVALS_URL,
    INSTRUCTOR_ELEMENT_ID,
    EVALS_DATA_PATH,
)

type BoxLike = tuple[int, int, int, int]


def _sanitize_filename(filename: str) -> str:
    """Removes punctuation and whitespace from teacher's
    names so they are acceptable as filenames.
    """
    sanitized = re.sub(r'[\\/*?:"<>|,]', "", filename)
    sanitized = sanitized.replace(' ', '_')
    return sanitized


def _crop_images_in_folder(source_folder: os.PathLike,
                          dest_folder: os.PathLike,
                          crop_coordinates: BoxLike) -> None:
    """Images show the entire gatorevals screen so they
    need to be cropped to focus on the chart.
    """
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


def _compress_images_in_folder(source_folder: os.PathLike,
                              dest_folder: os.PathLike,
                              quality: int = 60) -> None:
    """Compresses folder from around 500mb to 350mb.
    The setting for quality, set to 60 here, can be lowered
    or raised if needed.
    """
    # Create the destination folder if it doesn't exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Loop over all files in the directory
    for file_name in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file_name)
        if not file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue  # filter non-photos
        with Image.open(file_path) as img:
            # Convert the image to RGB mode
            if img.mode in {'RGBA', 'P'}:
                img = img.convert('RGB')

            # Construct the full path
            dest_file_path = os.path.join(dest_folder, file_name)
            
            # Save the image with the desired compression
            img.save(dest_file_path, quality=quality, optimize=True)
            print(f'Compressed image saved to {dest_file_path}')


def scrape_gator_evals() -> None:
    # Initialize the Selenium Chrome Driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    driver.get(GATOR_EVALS_URL)

    # Wait for the dropdown to be clickable and click it
    dropdown = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, 'tabZoneId12'))
    )
    dropdown.click()

    # Select each teacher in drop down menu one by one and take a screenshot
    for x in range(1, 5224):
        pyautogui.moveTo(x=990, y=425)  # hover over drop down menu scroller
        pyautogui.dragRel(xOffset=0, yOffset=570, button='PRIMARY', duration=3.0)

        element_id = INSTRUCTOR_ELEMENT_ID.format(x)  # Select teacher
        options = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, element_id))
        )
        options.click()
        # Find teacher's name
        element = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, element_id))
        )
        # Remove spaces and punctuation so it can be made into a file name
        element_text = element.text.strip()  # or element.text.strip()
        sanitized_text = _sanitize_filename(element_text)
        #Save screenshot to a file named after each teacher
        filename = f'{EVALS_DATA_PATH}{os.sep}{sanitized_text}.png'
        driver.save_screenshot(filename)
        # Wait for the dropdown to be clickable again and click it
        dropdown = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, 'tabZoneId12'))
        )
        dropdown.click()
        time.sleep(1)  # give time to load

    driver.quit()

    crop_coordinates = (0, 0, 1000, 825)  # (left, upper, right, lower)
    _crop_images_in_folder(EVALS_DATA_PATH, EVALS_DATA_PATH, crop_coordinates)
    _compress_images_in_folder(EVALS_DATA_PATH, EVALS_DATA_PATH, quality=60)
