from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Self

from .locations import ClassRoom
from .utils import check_types
from .textbook_collection import TextbookCollection


@dataclass(kw_only=True)
class Class:
    number: Optional[str]
    instructors: list[str]
    is_online: bool
    final_exam_time: Optional[tuple[datetime, datetime]]
    class_dates: tuple[datetime, datetime]
    textbooks: TextbookCollection
    classrooms: set[ClassRoom]
    locations: tuple[tuple[Optional[ClassRoom]]]
    
    def __post_init__(self) -> None:
        check_types(
            (self.number, Optional[str]),
            (self.instructors, list),
            (self.is_online, bool),
            (self.final_exam_time, Optional[tuple]),
            (self.class_dates, tuple),
            (self.textbooks, TextbookCollection),
            (self.classrooms, set),
            (self.locations, tuple),
        )

    def __hash__(self) -> int:
        return hash((self.number, tuple(self.instructors), self.locations))

    def __eq__(self, other: Self):
        if not isinstance(other, self.__class__):
            raise TypeError("`Class`' can only be compared "
                            "with other `Class` instances.")
        return hash(self) == hash(other)
