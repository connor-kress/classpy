from asyncio import Task
from typing import Optional, Self

from ..utils import check_types
from .textbook_info import TextbookInfo


class Textbook:
    link_cache: dict[TextbookInfo, Task[list[str]]] = {}

    def __init__(
        self,
        info: TextbookInfo,
        links: tuple[str],
        new_price: Optional[float],
        used_price: Optional[float],
    ) -> None:
        check_types(
            (info, TextbookInfo),
            (links, tuple),
            (new_price, Optional[float]),
            (used_price, Optional[float]),
        )
        self.info = info
        self.links = links
        self.new_price = new_price
        self.used_price = used_price
    
    def __repr__(self) -> str:
        return (f'{self.__class__.__name__}('
                    f'info={self.info}, '
                    f'links={self.links}, '
                    f'new_price={self.new_price}, '
                    f'used_price={self.used_price}'
                ')')

    def __hash__(self) -> int:
        return hash((self.info, self.links,
                     self.new_price, self.used_price))
    
    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError('`Textbook`s can only be compared '
                            'with other `Textbook` instances.')
        return hash(self) == hash(other)
