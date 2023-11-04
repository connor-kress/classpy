import asyncio
from playwright.async_api import async_playwright
from pprint import pprint

from classpy import *


async def main() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)

        # pprint(await course_query(browser, course_code='MAD2502'), depth=5)
        # pprint(await course_query(browser, course_code='COP'), depth=5)
        # pprint(await course_query(browser, course_code='MAC'), depth=5)
        # pprint(await course_query(browser, course_title='Programming Fundamentals 2'), depth=5)
        pprint(await course_query(browser, course_code='COP35'), depth=5)
        # pprint(await course_query(browser, course_code='MAD'), depth=5)
        # pprint(await course_query(browser, course_code='MAD', course_title='Computational'), depth=5)
        # pprint(await course_query(browser, term='2238', course_code='PHY2020'), depth=5)

        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
