from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .locations import ClassRoom
from .utils import check_types
from .textbook import Textbook


@dataclass(kw_only=True)
class Class:
    number: Optional[str]
    instructors: list[str]
    is_online: bool
    final_exam_time: Optional[tuple[datetime, datetime]]
    class_dates: tuple[datetime, datetime]
    textbooks: list[Textbook]
    locations: list[list[Optional[ClassRoom]]]
    
    def __post_init__(self) -> None:
        check_types(
            (self.number, Optional[str]),
            (self.instructors, list),
            (self.is_online, bool),
            (self.final_exam_time, Optional[tuple]),
            (self.class_dates, tuple),
            (self.textbooks, list),
            (self.locations, list),
        )
