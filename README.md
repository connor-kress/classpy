# ClassPy
<hr>
## Overview
<hr>
This is a basic UF API and schedule builder for UF students written in Python. The purpose of this module is to make it easier for students to view their available classes and to serve as an API for other programs.

## Installation
<hr>
### Installing Prerequisites
```
$ pip install playwright
$ pip install pyautogui
$ pip install webdriver_manager
$ pip install pillow
$ pip install bs4
$ pip install pandas
$ pip install selenium
$ pip install requests

$ playwright install
```
### Installing ClassPy
```
$ cd <DESIRED-PATH>
$ git clone https://github.com/connor-kress/classpy
$ pip install -e <PATH>
```
Note that `Python 3.12` is required to run ClassPy.

## Schedule Builder
<hr>

A basic terminal based schedule builder that allows users to make iterative queries to the UF Schedule of Courses with the `course_query` function through the asynchronous class-method `ScheduleBuilder.build` to build up a `Schedule` object.
```python
import asyncio
from classpy import ScheduleBuilder

async def main() -> None:
	schedule = await ScheduleBuilder.build()
	print(schedule)

if __name__ == '__main__':
	asyncio.run(main())
```
## Course Query API
<hr>

The primary course query API of the module, `course_query`, is a simple asynchronous function that returns a tuple of `Course` instances representing all results of the search in the UF Schedule of Courses.
```python
import asyncio
from classpy import course_query

async def main() -> None:
	courses = await course_query(code='MAD2502', ...)
	print(courses[0])

if __name__ == '__main__':
	asyncio.run(main())
```

## Gator Evals Scraping
<hr>

`GatorEvalsScraper.py` requires Selenium chrome-driver and the tableau link of the Gator Evals page `GatorEvalsScraper.py` works by first simulating a user inputted click on the `instructor_name` dropdown menu `pyautogui` is then used to simulate a click and drag on the scrollbar of the dropdown menu It then uses Selenium `webdriver` to iterate through each teacher and take a screenshot This screenshot is then renamed to the professor's name and cropped + compressed to focus the data This produces a folder to be used with the gator_evals_searcher.py gator_evals_searcher.py works by first accepting a user inputted instructor name It then searches through the folder provided by GatorEvalsScraper.py for a filename matching that user inputted name If the file is found, that file is selected and shown, if not, a string is returned reporting that no image was found.
