import asyncio
import pprint
from playwright.async_api import async_playwright

from classpy import *


async def main() -> None:
    # print = pprint.PrettyPrinter(depth=5).pprint
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        ctx = await browser.new_context()
        
        course = (await course_query(title='Programming fundamentals 2'))[0]
        print(course)

        await ctx.close()
        await browser.close()


if __name__ == '__main__':
    asyncio.run(main())
