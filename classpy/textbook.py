from asyncio import Task

from .utils import check_types
from .textbook_info import TextbookInfo


class Textbook:
    link_cache: dict[TextbookInfo, Task] = {}

    def __init__(self, info: TextbookInfo, links: list[str]) -> None:
        check_types(
            (info, TextbookInfo),
            (links, list),
        )
        self.info = info
        self.links = links
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.info}, {self.links})"
