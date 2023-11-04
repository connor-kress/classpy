from typing import Optional, Self
from dataclasses import dataclass


@dataclass(kw_only=True)
class TextbookInfo:
    title: Optional[str]
    author: Optional[str]
    isbn: Optional[str]

    def __post_init__(self) -> None:
        checks = (
            isinstance(self.title, Optional[str]),
            isinstance(self.author, Optional[str]),
            isinstance(self.isbn, Optional[str]),
        )
        if not all(checks):
            raise TypeError

    def __hash__(self) -> int:
        return hash((self.title, self.author, self.isbn))
    
    def __eq__(self, other: Self) -> bool:
        assert isinstance(other, self.__class__)
        return hash(self) == hash(other)
