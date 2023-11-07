import asyncio
from playwright.async_api import (
    async_playwright,
    Browser,
    Locator,
)
from typing import Optional, Any

from ..parsing import (
    parse_exam_time,
    parse_class_dates,
    parse_course_reqs,
)
from ..course import Course
from ..class_ import Class
from ..classroom import ClassRoom

from .textbook_data import get_textbooks_from_link

FALL_SPRING_PERIODS = 14
SUMMER_PERIODS = 9
DAY_OF_WEEK_DICT = {
    'M': 0,
    'T': 1,
    'W': 2,
    'R': 3,
    'F': 4,
    'S': 5,
}
FALL_SPRING_PERIOD_DICT = {
    '1': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    '10': 9,
    '11': 10,
    'E1': 11,
    'E2': 12,
    'E3': 13,
}
SUMMER_PERIOD_DICT = {
    '1': 0,
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    'E1': 7,
    'E2': 8,
}

SOC_BASE = 'https://one.uf.edu/soc/'
SS_PATH = r'C:\Users\con2c\Code\Comp. Math\Projects\classpy\classpy\data\images\{}.png'
DEFAULT_CATEGORY = 'CWSP'
DEFAULT_TERM = '2241'


async def course_query(
    browser: Optional[Browser] = None,
    *,
    category: str = DEFAULT_CATEGORY,
    term: str = DEFAULT_TERM,
    course_code: Optional[str] = None,
    course_title: Optional[str] = None,
    class_num: Optional[str] = None,
    instructor: Optional[str] = None,
    program_level: Optional[str] = None,
    department: Optional[str] = None,
) -> list[Course]:
    assert isinstance(category, str)
    assert isinstance(term, str)
    for arg in (course_code, course_title, class_num,
                instructor, program_level, department):
        assert isinstance(arg, Optional[str])
    if course_title is not None:
        course_title = course_title.replace(' ', '+')
    query_info = {
        'category': category,
        'term': term,
        'course-code': course_code,
        'course-title': course_title,
        'class-num': class_num,
        'instructor': instructor,
        'prog-level': program_level,
        'dept': department,
    }
    if browser is not None:
        return await _course_query_raw(browser, query_info)
    
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        result = await _course_query_raw(browser, query_info)
        await browser.close()
        return result

async def _course_query_raw(
    browser: Browser,
    query_info: dict[str, Optional[str]]
) -> list[Course]:
    soc_url = f'{SOC_BASE}?{'&'.join(f'{key}="{val}"'
                                    for key, val in query_info.items()
                                    if val is not None)}'
    page = await browser.new_page()
    await page.goto(soc_url)

    courses_locator = page.locator('.accordion__container')
    result_count = int(
        (await page.locator('div[aria-label="Search Results"] > div > p')
            .text_content())
            .removesuffix(' results')
    )
    if result_count > 1:
        await page.get_by_role("button", name="Expand All Courses").click()
    elif result_count == 0:
        await page.close()
        return []
    await courses_locator.nth(result_count-1).wait_for()
    # await page.screenshot(path=SS_PATH.format(query_info['course-code']))
    course_locators = await courses_locator.all()
    courses = await asyncio.gather(*(_scrape_course(browser, course) for course in course_locators))
    # courses = [await _scrape_course(browser, course) for course in course_locators]

    await page.close()
    return courses


async def _scrape_course(browser: Browser, course: Locator) -> Course:
    course_info = course.locator('//div[1]/div[1]/div')
    number, title = (
        await course_info.locator('//div[1]/div/p').text_content()
    ).split(' - ')
    description = await course_info.locator('//div[2]/p').text_content()
    prereq_str = await course_info.locator('//div[3]/p').text_content()
    requirements = parse_course_reqs(prereq_str.removeprefix('Prereq: '))
    classes_locator = course.locator('div.accordion__content > div')
    # await classes_locator.first.wait_for()
    offset_data = await _scrape_course_class_offset(classes_locator.first)
    class_locators = await classes_locator.all()
    print(f'{title} found {len(class_locators)} classes')
    classes = await asyncio.gather(*(_scrape_class(browser, class_) for class_ in class_locators))
    
    return Course(
        number=number,
        title=title,
        description=description,
        requirements=requirements,
        fees=offset_data['course_fees'],
        EEP_eligable=offset_data['EEP_eligable'],
        gen_ed=offset_data['gen_ed'],
        credits=offset_data['credits'],
        department=offset_data['department'],
        available_classes=classes,
    )


async def _scrape_class(browser: Browser, class_: Locator) -> Class:
    number = (await class_.locator('div[role="button"]')
                            .first
                            .text_content()
    ).removeprefix('Class #')
    if number == ' (Departmentally Controlled)':
        number = None
    box1 = class_.locator('//div[2]/div[1]')
    box2 = class_.locator('//div[2]/div[2]/div')

    location_locators = box1.locator('//div[1]/div/div[1]')
    locations = await _scrape_locations(browser, location_locators)
    instructors = await box2.locator('//div[1]/div[2]/div/p')\
                            .all_text_contents()
    is_online: bool
    match await box2.locator('//div[2]/div[2]/div/div[1]')\
                    .text_content():
        case 'Online (100%)': is_online = True
        case 'Primarily Classroom': is_online = False
        case _: raise Exception('Unmatched case')
    exam_time_str = await box2.locator('//div[5]/div[2]/div')\
                                .text_content()
    final_exam_time = parse_exam_time(exam_time_str)
    class_dates_str = await box2.locator('//div[6]/div[2]/div')\
                                .text_content()
    class_dates = parse_class_dates(class_dates_str)

    bsd_url = await box1.locator('a')\
                        .filter(has_text="Textbooks")\
                        .get_attribute('href')
    course_textbooks = await get_textbooks_from_link(browser, bsd_url)

    return Class(
        number=number,
        instructors=instructors,
        is_online=is_online,
        final_exam_time=final_exam_time,
        class_dates=class_dates,
        textbooks=course_textbooks,
        locations=locations,
    )


async def _scrape_course_class_offset(first_class: Locator) -> dict[str, Any]:
    box1 = first_class.locator('//div[2]/div[1]')
    box2 = first_class.locator('//div[2]/div[2]/div')
    additionals = await box1.locator('//div[3]')\
                            .get_by_role('button')\
                            .all_text_contents()
    course_fees = None
    EEP_eligable = False
    gen_ed = []
    for additional in additionals:
        if additional == 'EEP Eligible':
            EEP_eligable = True
        elif "Add'l Course Fees" in additional:
            course_fees = float(additional.removeprefix("Add'l Course Fees: $"))
        elif 'Gen Ed' in additional:
            gen_ed.append(additional.removeprefix('Gen Ed: '))
        else:
            raise Exception(f'"{additional}" additional case not handled.')
    
    credits = int(await box2.locator('//div[3]/div[2]/div')  # TODO: move to course_class_offset
                            .text_content())
    department = await box2.locator('//div[4]/div[2]/div')\
                            .text_content()
    
    return {
        'course_fees': course_fees,
        'EEP_eligable': EEP_eligable,
        'gen_ed': gen_ed,
        'credits': credits,
        'department': department,
    }

async def _scrape_locations(browser: Browser,
                            locations: Locator) -> list[list[ClassRoom]]:
    days_ = await locations.locator('//div[1]/div[1]').all_text_contents()
    periods = await locations.locator('//div[1]/div[2]').all_text_contents()
    room_locators =  locations.locator('//div[2]/div[1]/a')
    rooms = await room_locators.all_text_contents()
    links = await room_locators.all()
    schedule = list(list(None for _ in range(FALL_SPRING_PERIODS))
                         for _ in range(len(DAY_OF_WEEK_DICT)))
    for days, period, room, link in zip(days_, periods, rooms, links):
        days = days.removesuffix('\xa0|\xa0').split(',')
        period = period.removeprefix('Period ')\
                       .removeprefix('Periods ')\
                       .removesuffix('\xa0')
        room = room.removesuffix('\xa0launch')
        url = await link.get_attribute('href')
        day_idxs = tuple(DAY_OF_WEEK_DICT[day] for day in days)
        period_idxs: tuple[int]
        if '-' in period:
            start, end = period.split('-')
            period_idxs = tuple(range(FALL_SPRING_PERIOD_DICT[start],
                                      FALL_SPRING_PERIOD_DICT[end]+1))
        else:
            period_idxs = (FALL_SPRING_PERIOD_DICT[period],)
        for day_idx in day_idxs:
            for period_idx in period_idxs:
                schedule[day_idx][period_idx] = ClassRoom(room, url)

    return schedule
