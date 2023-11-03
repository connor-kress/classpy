from abc import ABC, abstractmethod
from typing import Iterable, Self


class BooleanExpr(ABC):
    @abstractmethod
    def eval(self, values: Iterable[str]) -> bool:
        """Evaluates the boolean value of the expression
        given that all passes `values` are true.
        """
    
    @abstractmethod
    def given(self, values: Iterable[str]) -> Self:
        """Returns a new boolean expression representing the
        missing values, given that all passes `values` are true
        and the expression does not evaluate to true given them
        (`self.eval(values) != True`).
        """


class BooleanToken(BooleanExpr):
    def __init__(self, value: str) -> None:
        assert isinstance(value, str)
        self.value = value
    
    def eval(self, values: Iterable[str]) -> bool:
        return self.value in values
    
    def given(self, values: Iterable[str]) -> BooleanExpr:
        assert self.value not in values
        return self
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.value}')"
    
    def inside_str(self) -> str:
        return self.value
    
    def __str__(self) -> str:
        return self.value


class BooleanAnd(BooleanExpr):
    def __init__(self, *values: BooleanExpr) -> None:
        assert isinstance(values, tuple)
        self.values = values
    
    def eval(self, values: Iterable[str]) -> bool:
        return all(val.eval(values) for val in self.values)
    
    def given(self, values: Iterable[str]) -> BooleanExpr:
        new_values = tuple(val.given(values)
                           for val in self.values
                           if not val.eval(values))
        assert new_values
        if len(new_values) == 1:
            return new_values[0]
        return self.__class__(*new_values)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}'\
               f'({', '.join(map(repr, self.values))})'
    
    def inside_str(self) -> str:
        return f'({str(self)})'
    
    def __str__(self) -> str:
        return ' and '.join(val.inside_str() for val in self.values)


class BooleanOr(BooleanExpr):
    def __init__(self, *values: BooleanExpr) -> None:
        assert isinstance(values, tuple)
        self.values = values
    
    def eval(self, values: Iterable[str]) -> bool:
        return any(val.eval(values) for val in self.values)
    
    def given(self, values: Iterable[str]) -> BooleanExpr:
        assert not self.eval(values)
        new_values = tuple(val.given(values) for val in self.values)
        if len(new_values) == 1:
            return new_values[0]
        return self.__class__(*new_values)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}'\
               f'({', '.join(map(repr, self.values))})'
    
    def inside_str(self) -> str:
        return f'({str(self)})'
    
    def __str__(self) -> str:
        return ' or '.join(val.inside_str() for val in self.values)


def main() -> None:
    a = BooleanToken('a')
    b = BooleanToken('b')
    c = BooleanToken('c')
    d = BooleanToken('d')

    expr = BooleanOr(BooleanAnd(BooleanOr(a, b), c, d), b)
    print(expr)
    print(repr(expr))
    # print(expr.given(['a']))
    # print(expr.given(['a', 'c']))
    # print(expr.given(['c']))


if __name__ == '__main__':
    main()
