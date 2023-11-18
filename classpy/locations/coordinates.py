from dataclasses import dataclass
from typing import Self

from ..utils import check_types


@dataclass
class Coords:
    lat: float
    lon: float

    def __post_init__(self) -> None:
        check_types(
            (self.lat, float),
            (self.lon, float),
        )
    
    def __hash__(self) -> int:
        return hash((self.lat, self.lon))
    
    def __eq__(self, other: Self):
        if not isinstance(other, self.__class__):
            raise TypeError('`Coords`s can only be compared '
                            'with other `Coords` instances.')
        return hash(self) == hash(other)
