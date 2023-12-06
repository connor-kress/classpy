import asyncio
from collections.abc import Awaitable
from playwright.async_api import BrowserContext
import playwright
from typing import Literal, Optional

from ..textbook_collection import TextbookCollection
from ..textbook_info import TextbookInfo
from ..textbook import Textbook

type _ReqLevel = Literal['required', 'optional', 'recommended']
_req_levels = ('required', 'optional', 'recommended')


class TextbookManager:
    def __init__(self) -> None:
        self.required: list[Awaitable[Textbook]] = []
        self.optional: list[Awaitable[Textbook]] = []
        self.recommended: list[Awaitable[Textbook]] = []
    
    def add(self, coro: Awaitable[Textbook], req_level: _ReqLevel):
        if not req_level in _req_levels:
            raise ValueError('`req_level` parameter of `TextbookManager.add` '
                             f'does not accept the value "{req_level}".')
        match req_level:
            case 'required':
                self.required.append(coro)
            case 'optional':
                self.optional.append(coro)
            case 'recommended':
                self.recommended.append(coro)
    
    async def collect(self) -> TextbookCollection:
        required = asyncio.gather(*self.required)
        optional = asyncio.gather(*self.optional)
        recommended = asyncio.gather(*self.recommended)
        required, optional, recommended = \
            await asyncio.gather(required, optional, recommended)
        return TextbookCollection(
            required=tuple(required),
            optional=tuple(optional),
            recommended=tuple(recommended),
        )


async def get_textbooks_from_link(ctx: BrowserContext,
                                  bsd_url: str) -> list[Textbook]:
    print(f'opening {bsd_url}')
    page = await ctx.new_page()
    try:
        await page.goto(bsd_url, timeout=240_000)
    except Exception as e:
        print(f'Failed to open {bsd_url}')
        raise e
    rows = await page.locator('table[class="books"] > tbody > tr').all()
    start_idxs = [i for i, loc in enumerate(rows)
                  if 'Title:' in await loc.inner_text()]
    textbook_manager = TextbookManager()
    textbook_infos = set[TextbookInfo]()
    for i in start_idxs:
        title, isbn_raw, cover_raw = (
            await rows[i].locator('td[class="books"]').all_text_contents()
        )[:3]
        isbn: Optional[str] = None
        if isbn_raw.strip() != 'UFALLACCESS':
            isbn = isbn_raw.strip() or None
        cover: Optional[str] = None
        if cover_raw.strip() != 'N/A':
            cover = cover_raw.strip()
        author, edition, copyright, publisher = (
            await rows[i+1].locator('td[class="books"]').all_text_contents()
        )[:4]
        prices = await rows[i+2].locator('td[class="books"] > span')\
                                .all_text_contents()
        if prices:
            new_price = float(prices[0].removeprefix('$'))
            used_price = float(prices[1].removeprefix('$'))
        else:
            new_price, used_price = None, None
        req_level = (await rows[i+3].locator('//td[3]/span')\
                                    .text_content())\
                                    .replace('\xa0', '')\
                                    .removeprefix('This text is ')
        textbook_info = TextbookInfo(
            title=title.strip() or None,
            isbn=isbn,
            cover=cover,
            author=author.strip() or None,
            edition=edition.strip() or None,
            copyright=copyright.strip() or None,
            publisher=publisher.strip() or None,
        )
        if textbook_info in textbook_infos:
            continue
        textbook_infos.add(textbook_info)
        textbook_coro = _get_textbook_from_info(ctx, textbook_info,
                                                new_price, used_price)
        textbook_manager.add(textbook_coro, req_level)

    await page.close()
    return await textbook_manager.collect()


async def _get_textbook_from_info(
    ctx: BrowserContext,
    info: TextbookInfo,
    new_price: Optional[float],
    used_price: Optional[float],
) -> Textbook:
    if info in Textbook.link_cache:
        print(f'cache hit on {info.title}')
        links = await Textbook.link_cache[info]
        return Textbook(info, links, new_price, used_price)
    links_task = asyncio.ensure_future(_get_links_from_info(ctx, info))
    Textbook.link_cache[info] = links_task
    links = await links_task
    return Textbook(info, links, new_price, used_price)


async def _get_links_from_info(ctx: BrowserContext, info: TextbookInfo) -> tuple[str]:
    print(f'searching libgen for {info.title}')
    page = await ctx.new_page()
    # page.goto('https://www.libgen.li/...')
    ...
    await asyncio.sleep(1)
    links: tuple[str] = ()  # TODO

    await page.close()
    return links
