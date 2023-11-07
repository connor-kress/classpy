from typing import Optional, Self
from dataclasses import dataclass

from .utils import check_types


@dataclass(kw_only=True)
class TextbookInfo:
    title: Optional[str]
    author: Optional[str]
    isbn: Optional[str]

    def __post_init__(self) -> None:
        check_types(
            (self.title, Optional[str]),
            (self.author, Optional[str]),
            (self.isbn, Optional[str]),
        )

    def __hash__(self) -> int:
        return hash((self.title, self.author, self.isbn))
    
    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError('`TextbookInfo`s can only be compared '
                            'with other `TextbookInfo` instances.')
        return hash(self) == hash(other)
