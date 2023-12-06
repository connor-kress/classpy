import asyncio
from playwright.async_api import (
    async_playwright,
    BrowserContext,
    Locator,
)
from typing import Optional, Any

from ..data.raw_data import (
    SOC_BASE,
    SS_PATH,
    DEFAULT_CATEGORY,
    DEFAULT_TERM,
    WEEK_DAYS,
    FALL_SPRING_PERIODS,
    DAY_OF_WEEK_DICT,
    FALL_SPRING_PERIOD_DICT,
)
from ..parsing import (
    parse_exam_time,
    parse_class_dates,
    parse_course_reqs,
)
from ..core import Course, Class
from ..locations import ClassRoom
from ..data import get_building
from ..utils import check_types

from .textbook_data import get_textbooks_from_link

from ..class_functions import add_class_course_binding


async def course_query(
    ctx: Optional[BrowserContext] = None,
    *,
    category: str = DEFAULT_CATEGORY,
    term: str = DEFAULT_TERM,
    code: Optional[str] = None,
    title: Optional[str] = None,
    class_num: Optional[str] = None,
    instructor: Optional[str] = None,
    program_level: Optional[str] = None,
    department: Optional[str] = None,
) -> tuple[Course]:
    """Scrapes the UF Schedule of Courses with the specified search parameters.
    Returns all matches in the form of `Course` objects.

    ### Parameters
    * `ctx`: pass a playwright async `BrowserContext` to use it for the search.
    If no context is passed, a new chromium instance will be created and ended
    for the query.
    """
    check_types(
        (category, str),
        (term, str),
        (code, Optional[str]),
        (title, Optional[str]),
        (class_num, Optional[str]),
        (instructor, Optional[str]),
        (program_level, Optional[str]),
        (department, Optional[str]),
    )
    if title is not None:
        title = title.replace(' ', '+')
    query_info = {
        'category': category,
        'term': term,
        'course-code': code,
        'course-title': title,
        'class-num': class_num,
        'instructor': instructor,
        'prog-level': program_level,
        'dept': department,
    }
    if ctx is not None:
        return await _course_query_raw(ctx, query_info)
    
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        ctx = await browser.new_context()
        result = await _course_query_raw(ctx, query_info)
        await ctx.close()
        await browser.close()
        return result


async def _course_query_raw(
    ctx: BrowserContext,
    query_info: dict[str, Optional[str]]
) -> tuple[Course]:
    """Non user-friendly `course_query` which requires a `ctx` argument."""
    soc_url = f'{SOC_BASE}?{'&'.join(f'{key}="{val}"'
                                    for key, val in query_info.items()
                                    if val is not None)}'
    page = await ctx.new_page()
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
    # ss_path = f'{SS_PATH}{query_info['course-code']}.png'
    # await page.screenshot(path=ss_path)
    course_locators = await courses_locator.all()
    courses = await asyncio.gather(*(_scrape_course(ctx, course) for course in course_locators))
    # courses = [await _scrape_course(ctx, course) for course in course_locators]

    await page.close()
    return tuple(courses)


async def _scrape_course(ctx: BrowserContext, course: Locator) -> Course:
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
    print(f'Found {len(class_locators)} classes for {title}')
    classes = tuple(await asyncio.gather(*(_scrape_class(ctx, class_)
                                           for class_ in class_locators)))
    course = Course(
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
    for class_ in classes:
        add_class_course_binding(class_, course)
    return course


async def _scrape_class(ctx: BrowserContext, class_: Locator) -> Class:
    number = (await class_.locator('div[role="button"]')
                            .first
                            .text_content()
    ).removeprefix('Class #')
    if number == ' (Departmentally Controlled)':
        number = None
    box1 = class_.locator('//div[2]/div[1]')
    box2 = class_.locator('//div[2]/div[2]/div')

    location_locators = box1.locator('//div[1]/div/div[1]')
    classrooms, locations = await _scrape_locations(location_locators)
    instructors = tuple(await box2.locator('//div[1]/div[2]/div/p')\
                                  .all_text_contents())
    is_online: bool
    match await box2.locator('//div[2]/div[2]/div/div[1]')\
                    .first.text_content():
        case 'Online (100%)': is_online = True
        case 'Online (80-99%)': is_online = True
        case 'Primarily Classroom': is_online = False
        case 'Hybrid': is_online = False
        case _: raise Exception(f'Unmatched case (class # {number})')
    exam_time_str = await box2.locator('//div[5]/div[2]/div')\
                                .text_content()
    final_exam_time = parse_exam_time(exam_time_str)
    class_dates_str = await box2.locator('//div[6]/div[2]/div')\
                                .text_content()
    class_dates = parse_class_dates(class_dates_str)

    bsd_url = await box1.locator('a')\
                        .filter(has_text="Textbooks")\
                        .get_attribute('href')
    course_textbooks = await get_textbooks_from_link(ctx, bsd_url)

    return Class(
        number=number,
        instructors=instructors,
        is_online=is_online,
        final_exam_time=final_exam_time,
        class_dates=class_dates,
        textbooks=course_textbooks,
        classrooms=classrooms,
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
    gen_ed = list[str]()
    for additional in additionals:
        if additional == 'EEP Eligible':
            EEP_eligable = True
        elif "Add'l Course Fees" in additional:
            course_fees = float(additional.removeprefix("Add'l Course Fees: $"))
        elif 'Gen Ed' in additional:
            gen_ed.append(additional.removeprefix('Gen Ed: '))
        else:
            raise Exception(f'"{additional}" additional case not handled.')
    gen_ed = tuple(gen_ed)
    
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

async def _scrape_locations(
    locations: Locator
) -> tuple[frozenset[ClassRoom], tuple[tuple[Optional[ClassRoom], ...], ...]]:
    classrooms = set[ClassRoom]()
    days_ = await locations.locator('//div[1]/div[1]').all_text_contents()
    periods = await locations.locator('//div[1]/div[2]').all_text_contents()
    room_codes = await locations.locator('//div[2]/div[1]/a').all_text_contents()
    schedule: list[list[Optional[ClassRoom]]] = [
        [None for _ in range(FALL_SPRING_PERIODS)]
        for _ in range(WEEK_DAYS)
    ]
    for days, period, room_code in zip(days_, periods, room_codes):
        days = days.removesuffix('\xa0|\xa0').split(',')
        period = period.removeprefix('Period ')\
                       .removeprefix('Periods ')\
                       .removesuffix('\xa0')
        room_code = room_code.removesuffix('\xa0launch')
        day_idxs = tuple(DAY_OF_WEEK_DICT[day] for day in days)
        period_idxs: tuple[int]
        if '-' in period:
            start, end = period.split('-')
            period_idxs = tuple(range(FALL_SPRING_PERIOD_DICT[start],
                                      FALL_SPRING_PERIOD_DICT[end]+1))
        else:
            period_idxs = (FALL_SPRING_PERIOD_DICT[period],)
        building_abbrev, room_number = room_code.split(' ')
        building = get_building(building_abbrev)
        if building is None:
            raise Exception(f'"{building_abbrev}" could not be found.')
        classroom = ClassRoom(
            code=room_code,
            number=room_number,
            building=building,
        )
        classrooms.add(classroom)
        for day_idx in day_idxs:
            for period_idx in period_idxs:
                schedule[day_idx][period_idx] = classroom
    
    schedule_tuple = tuple(tuple(row) for row in schedule)
    return frozenset(classrooms), schedule_tuple
