from typing import Optional, Self
from dataclasses import dataclass

from .utils import check_types


@dataclass(kw_only=True)
class TextbookInfo:
    title: Optional[str]
    isbn: Optional[str]
    cover: Optional[str]
    author: Optional[str]
    edition: Optional[str]
    copyright: Optional[str]
    publisher: Optional[str]

    def __post_init__(self) -> None:
        check_types(
            (self.title, Optional[str]),
            (self.isbn, Optional[str]),
            (self.cover, Optional[str]),
            (self.author, Optional[str]),
            (self.edition, Optional[str]),
            (self.copyright, Optional[str]),
            (self.publisher, Optional[str]),
        )

    def __hash__(self) -> int:
        return hash((
            self.title, self.isbn, self.cover,
            self.author, self.edition,
            self.copyright, self.publisher,
        ))
    
    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, self.__class__):
            raise TypeError('`TextbookInfo`s can only be compared '
                            'with other `TextbookInfo` instances.')
        return hash(self) == hash(other)
