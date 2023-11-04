from dataclasses import dataclass
from typing import Optional

from .utils import BooleanExpr


@dataclass
class CourseReq:
    string: str
    expr: Optional[BooleanExpr]
    extra_and: Optional[str]
    extra_or: Optional[str]

    def __post_init__(self) -> None:
        checks = (
            isinstance(self.string, str),
            isinstance(self.expr, Optional[BooleanExpr]),
            isinstance(self.extra_and, Optional[str]),
            isinstance(self.extra_or, Optional[str]),
        )
        if not all(checks):
            raise TypeError
    
    def __str__(self) -> str:
        if self.expr is None:
            return self.string
        acc = str(self.expr)
        if self.extra_and is not None:
            acc += f'(and {self.extra_and})'
        if self.extra_or is not None:
            acc += f'(or {self.extra_or})'
        return acc
