from typing import Optional

from .utils import BooleanExpr


class CourseReq:
    def __init__(self, string: str, expr: Optional[BooleanExpr],
                 extra_and: Optional[str], extra_or: Optional[str]) -> None:
        assert isinstance(string, str)
        assert isinstance(expr, Optional[BooleanExpr])
        assert isinstance(extra_and, Optional[str])
        assert isinstance(extra_or, Optional[str])
        self.string = string
        self.expr = expr
        self.extra_and = extra_and
        self.extra_or = extra_or
    
    def __repr__(self) -> str:
        extra_and_str = 'None' if self.extra_and is None else f"'{self.extra_and}'"
        extra_or_str = 'None' if self.extra_or is None else f"'{self.extra_or}'"
        return f"{self.__class__.__name__}("\
            f"'{self.string}', {repr(self.expr)}, "\
            f"{extra_and_str}, {extra_or_str})"

    def __str__(self) -> str:
        if self.expr is None:
            return self.string
        acc = str(self.expr)
        if self.extra_and is not None:
            acc += f'(and {self.extra_and})'
        if self.extra_or is not None:
            acc += f'(or {self.extra_or})'
        return acc
