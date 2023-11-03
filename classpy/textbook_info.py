from typing import Optional, Self


class TextbookInfo:
    def __init__(
        self,
        title: Optional[str],
        author: Optional[str],
        isbn: Optional[str],
    ) -> None:
        for arg in (title, author, isbn):
            assert isinstance(arg, Optional[str])
        self.title = title
        self.author = author
        self.isbn = isbn
    
    def __repr__(self) -> str:
        title_str = 'None' if self.title is None else f"'{self.title}'"
        author_str = 'None' if self.author is None else f"'{self.author}'"
        isbn_str = 'None' if self.isbn is None else f"'{self.isbn}'"
        return f"{self.__class__.__name__}({title_str}, {author_str}, {isbn_str})"

    def __hash__(self) -> int:
        return hash((self.title, self.author, self.isbn))
    
    def __eq__(self, other: Self) -> bool:
        assert isinstance(other, self.__class__)
        return hash(self) == hash(other)
