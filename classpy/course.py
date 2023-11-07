from dataclasses import dataclass
from typing import Optional

from .course_req import CourseReq
from .class_ import Class
from .utils import check_types


@dataclass(kw_only=True)
class Course:
    number: str
    title: str
    description: str
    requirements: CourseReq
    fees: Optional[float]
    EEP_eligable: bool
    gen_ed: list[str]
    credits: int
    department: str
    available_classes: list[Class]

    def __post_init__(self) -> None:
        check_types(
            (self.number, str),
            (self.title, str),
            (self.description, str),
            (self.requirements, CourseReq),
            (self.fees, Optional[float]),
            (self.EEP_eligable, bool),
            (self.gen_ed, list),
            (self.credits, int),
            (self.department, str),
            (self.available_classes, list),
        )
