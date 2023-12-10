from dataclasses import dataclass
from typing import Self

from .coordinates import Coords
from ..utils import check_types


@dataclass(kw_only=True)
class BusStop:
    id: str
    name: str
    description: str
    coords: Coords

    def __post_init__(self) -> None:
        check_types(
            (self.id, str),
            (self.name, str),
            (self.description, str),
            (self.coords, Coords),
        )

    def __hash__(self) -> int:
        return hash(self.id)
    
    def __eq__(self, other: Self):
        if not isinstance(other, self.__class__):
            raise TypeError('`BusStop`s can only be compared '
                            'with other `BusStop` instances.')
        return hash(self) == hash(other)
