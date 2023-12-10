from dataclasses import dataclass
from typing import Self

from .building import Building
from ..utils import check_types


@dataclass(kw_only=True)
class ClassRoom:
    code: str
    number: str
    building: Building

    def __post_init__(self) -> None:
        check_types(
            (self.code, str),
            (self.number, str),
            (self.building, Building),
        )
    
    def __hash__(self) -> int:
        return hash(self.code)

    def __eq__(self, other: Self):
        if not isinstance(other, self.__class__):
            raise TypeError('`ClassRoom`s can only be compared '
                            'with other `ClassRoom` instances.')
        return hash(self) == hash(other)
