import asyncio
import pprint
from playwright.async_api import async_playwright

from classpy import *


async def main() -> None:
    pprint = pprint.PrettyPrinter(depth=5).pprint
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)

        # pprint(await course_query(browser, course_code='MAD2502'))
        pprint(await course_query(browser, course_code='COP'))
        # pprint(await course_query(browser, course_code='MAC'))
        # pprint(await course_query(browser, course_title='Programming Fundamentals 2'))
        # pprint(await course_query(browser, course_code='COP35'))
        # pprint(await course_query(browser, course_code='MAD'))
        # pprint(await course_query(browser, course_code='MAD', course_title='Computational'))
        # pprint(await course_query(browser, term='2238', course_code='PHY2020'))

        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
