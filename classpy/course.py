from typing import Optional

from .utils import BooleanExpr
from .course_req import CourseReq
from .class_ import Class


class Course:
    def __init__(
            self,
            *,
            number: str,
            title: str,
            description: str,
            requirements: CourseReq,
            fees: Optional[float],
            EEP_eligable: bool,
            gen_ed: list[str],
            available_classes: list[Class],
        ) -> None:
        assert isinstance(number, str)
        assert isinstance(title, str)
        assert isinstance(description, str)
        assert isinstance(requirements, CourseReq)
        assert isinstance(fees, Optional[float])
        assert isinstance(EEP_eligable, bool)
        assert isinstance(gen_ed, list)
        assert isinstance(available_classes, list)
        self.number = number
        self.title = title
        self.description = description
        self.requirements = requirements
        self.fees = fees
        self.EEP_eligable = EEP_eligable
        self.gen_ed = gen_ed
        self.available_classes = available_classes
    
    def __repr__(self) -> str:
        return f'''{self.__class__.__name__}(
            number='{self.number}',
            title='{self.title}',
            description='{self.description}',
            requirements={repr(self.requirements)},
            fees={self.fees},
            EEP_eligable={self.EEP_eligable},
            gen_ed={self.gen_ed},
            available_classes={self.available_classes},
        )'''