from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .classroom import ClassRoom
from .textbook import Textbook


@dataclass(kw_only=True)
class Class:
    number: Optional[str]
    instructors: list[str]
    is_online: bool
    credits: int
    department: str
    final_exam_time: Optional[tuple[datetime, datetime]]
    class_dates: tuple[datetime, datetime]
    textbooks: list[Textbook]
    locations: list[list[ClassRoom]]
    
    def __post_init__(self) -> None:
        checks = (
            isinstance(self.number, Optional[str]),
            isinstance(self.instructors, list),
            isinstance(self.is_online, bool),
            isinstance(self.credits, int),
            isinstance(self.department, str),
            isinstance(self.final_exam_time, Optional[tuple]),
            isinstance(self.class_dates, tuple),
            isinstance(self.textbooks, list),
            isinstance(self.locations, list),
        )
        if not all(checks):
            raise TypeError
