import asyncio
from playwright.async_api import async_playwright
from classpy import course_query

from classpy import Course, Class, Textbook, TextbookInfo, BooleanToken, BooleanAnd, BooleanOr
import datetime

async def main() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)

        # print(await course_query(browser, course_code='MAD2502'))
        # print(await course_query(browser, course_code='COP'))
        # print(await course_query(browser, course_code='MAC'))
        # print(await course_query(browser, course_title='Programming Fundamentals 2'))
        print(await course_query(browser, course_code='COP35'))
        # print(await course_query(browser, course_code='MAD'))
        # print(await course_query(browser, course_code='MAD', course_title='Computational'))
        print(await course_query(browser, term='2238', course_code='PHY2020'))

        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
