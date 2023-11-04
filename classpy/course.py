from typing import Optional
from dataclasses import dataclass

from .course_req import CourseReq
from .class_ import Class


@dataclass(kw_only=True)
class Course:
    number: str
    title: str
    description: str
    requirements: CourseReq
    fees: Optional[float]
    EEP_eligable: bool
    gen_ed: list[str]
    available_classes: list[Class]

    def __post_init__(self) -> None:
        checks = (  
            isinstance(self.number, str),
            isinstance(self.title, str),
            isinstance(self.description, str),
            isinstance(self.requirements, CourseReq),
            isinstance(self.fees, Optional[float]),
            isinstance(self.EEP_eligable, bool),
            isinstance(self.gen_ed, list),
            isinstance(self.available_classes, list),
        )
        if not all(checks):
            raise TypeError
    
    # def __repr__(self) -> str:
    #     return f'''{self.__class__.__name__}(
    #         number={repr(self.number)},
    #         title={repr(self.title)},
    #         description={repr(self.description)},
    #         requirements={repr(self.requirements)},
    #         fees={repr(self.fees)},
    #         EEP_eligable={repr(self.EEP_eligable)},
    #         gen_ed={repr(self.gen_ed)},
    #         available_classes={repr(self.available_classes)},
    #     )'''
