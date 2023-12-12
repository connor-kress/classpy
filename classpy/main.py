import asyncio
from pprint import pprint
from playwright.async_api import async_playwright

from classpy import *


async def main() -> None:
    # course = (await course_query(title='Programming fundamentals 2'))[0]
    # pprint(course)

    schedule = await ScheduleBuider.build()
    print(schedule)


if __name__ == '__main__':
    asyncio.run(main())
