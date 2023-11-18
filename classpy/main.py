import asyncio
import pprint
from playwright.async_api import async_playwright

from classpy import *


async def main() -> None:
    # print = pprint.PrettyPrinter(depth=5).pprint
    # async with async_playwright() as playwright:
    #     browser = await playwright.chromium.launch(headless=True)
    #     ctx = await browser.new_context()

    #     print(await course_query(ctx, course_code='MAD2502'))
    #     # print(await course_query(ctx, course_code='COP'))
    #     # print(await course_query(ctx, term='2238', course_code='PHY2020'))

    #     await ctx.close()
    #     await browser.close()

    course = (await course_query(course_title='Programming fundamentals 2'))[0]
    for class_ in course.available_classes:
        assert get_course_of(class_) is course
    print(course)


if __name__ == '__main__':
    asyncio.run(main())
