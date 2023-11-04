import asyncio
from playwright.async_api import Browser

from ..textbook_info import TextbookInfo
from ..textbook import Textbook


async def get_textbooks_from_link(browser: Browser, bsd_url: str) -> list[Textbook]:
    textbook_data = await _get_textbook_infos_from_link(browser, bsd_url)
    textbook_futures = [_get_textbook_from_info(browser, info)
                        for info in textbook_data]
    return await asyncio.gather(*textbook_futures)
    


async def _get_textbook_infos_from_link(browser: Browser, bsd_url: str) -> list[TextbookInfo]:
    print(f'opening {bsd_url}')
    page = await browser.new_page()
    await page.goto(bsd_url)

    ...

    await page.close()
    return [TextbookInfo('Diary of a Wimpy Kid', 'Jeff Kinney', '2836423')]


async def _get_textbook_from_info(browser: Browser, info: TextbookInfo) -> Textbook:
    if info in Textbook.link_cache:
        print(f'cache hit on {info.title}')
        links = await Textbook.link_cache[info]
        return Textbook(info, links)
    links_task = asyncio.ensure_future(_get_links_from_info(browser, info))
    Textbook.link_cache[info] = links_task
    links = await links_task
    return Textbook(info, links)


async def _get_links_from_info(browser: Browser, info: TextbookInfo) -> Textbook:
    print(f'searching libgen for {info.title}')
    page = await browser.new_page()
    # page.goto('https://www.libgen.li/...')
    ...
    await asyncio.sleep(1)
    links = []  # TODO

    await page.close()
    return links
