from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Self, Literal

from ..locations import ClassRoom
from ..utils import check_types
from .textbook_collection import TextbookCollection

type ClassType = Literal['Primarily Classroom', 'Online (100%)', 'Online (80-99%)', 'Hybrid']


@dataclass(kw_only=True, frozen=True)
class Class:
    number: Optional[str]
    instructors: tuple[str, ...]
    is_online: bool
    type_: ClassType
    final_exam_time: Optional[tuple[datetime, datetime]]
    class_dates: tuple[datetime, datetime]
    textbooks: TextbookCollection
    classrooms: frozenset[ClassRoom]
    locations: tuple[tuple[Optional[ClassRoom], ...], ...]
    
    def __post_init__(self) -> None:
        check_types(
            (self.number, Optional[str]),
            (self.instructors, tuple),
            (self.is_online, bool),
            (self.type_, str),
            (self.final_exam_time, Optional[tuple]),
            (self.class_dates, tuple),
            (self.textbooks, TextbookCollection),
            (self.classrooms, frozenset),
            (self.locations, tuple),
        )

    def __eq__(self, other: Self):
        if not isinstance(other, self.__class__):
            raise TypeError("`Class`' can only be compared "
                            "with other `Class` instances.")
        return hash(self) == hash(other)
