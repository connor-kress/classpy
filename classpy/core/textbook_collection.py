from dataclasses import dataclass

from ..utils import check_types
from .textbook import Textbook


@dataclass(kw_only=True, frozen=True)
class TextbookCollection:
    required: tuple[Textbook]
    optional: tuple[Textbook]
    recommended: tuple[Textbook]

    def __post_init__(self) -> None:
        check_types(
            (self.required, tuple),
            (self.optional, tuple),
            (self.recommended, tuple),
        )
