from datetime import datetime
from typing import Optional

from .classroom import ClassRoom
from .textbook import Textbook


class Class:
    def __init__(
            self,
            *,
            number: Optional[str],
            instructors: list[str],
            is_online: bool,
            credits: int,
            department: str,
            final_exam_time: Optional[tuple[datetime, datetime]],
            class_dates: tuple[datetime, datetime],
            textbooks: list[Textbook],
            locations: list[list[ClassRoom]]
        ) -> None:
        assert isinstance(number, Optional[str])
        assert isinstance(instructors, list)
        assert isinstance(is_online, bool)
        assert isinstance(credits, int)
        assert isinstance(department, str)
        assert isinstance(final_exam_time, Optional[tuple])
        assert isinstance(class_dates, tuple)
        assert isinstance(textbooks, list)
        assert isinstance(locations, list)
        self.number = number
        self.instructors = instructors
        self.is_online = is_online
        self.credits = credits
        self.department = department
        self.final_exam_time = final_exam_time
        self.class_dates = class_dates
        self.textbooks = textbooks
        self.locations = locations

    def __repr__(self) -> str:
        number_str = 'None' if self.number is None else f"'{self.number}'"
        return f'''{self.__class__.__name__}(
            number={number_str},
            instructors={self.instructors},
            is_online={self.is_online},
            credits={self.credits},
            department='{self.department}',
            final_exam_time={self.final_exam_time},
            class_dates={self.class_dates},
            textbooks={self.textbooks},
            locations={self.locations},
        )'''
