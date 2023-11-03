from typing import Optional

from .utils import BooleanExpr
from .class_ import Class


class Course:
    def __init__(
            self,
            *,
            number: str,
            title: str,
            description: str,
            prereq_str: str,
            prereq_expr: Optional[BooleanExpr],
            prereq_extra_and: Optional[str],
            prereq_extra_or: Optional[str],
            available_classes: list[Class],
        ) -> None:
        assert isinstance(number, str)
        assert isinstance(title, str)
        assert isinstance(description, str)
        assert isinstance(prereq_str, str)
        assert isinstance(prereq_expr, Optional[BooleanExpr])
        assert isinstance(prereq_extra_and, Optional[str])
        assert isinstance(prereq_extra_or, Optional[str])
        assert isinstance(available_classes, list)
        self.number = number
        self.title = title
        self.description = description
        self.prereq_str = prereq_str
        self.prereq_expr = prereq_expr
        self.prereq_extra_and = prereq_extra_and
        self.prereq_extra_or = prereq_extra_or
        self.available_classes = available_classes
    
    def __repr__(self) -> str:
        prereq_extra_and_str = 'None' if self.prereq_extra_and is None\
                                else f"'{self.prereq_extra_and}'"
        prereq_extra_or_str = 'None' if self.prereq_extra_and is None\
                               else f"'{self.prereq_extra_and}'"
        return f'''{self.__class__.__name__}(
            number='{self.number}',
            title='{self.title}',
            description='{self.description}',
            prereq_str='{self.prereq_str}',
            prereq_expr={repr(self.prereq_expr)},
            prereq_extra_and={prereq_extra_and_str},
            prereq_extra_or={prereq_extra_or_str},
            available_classes={self.available_classes},
        )'''