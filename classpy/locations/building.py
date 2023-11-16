from dataclasses import dataclass
from typing import Optional, Self

from .coordinates import Coords
from ..utils import check_types


@dataclass(kw_only=True)
class Building:
    id: str
    name: str
    common_name: Optional[str]
    abbrev: Optional[str]
    coords: Coords

    def __post_init__(self) -> None:
        check_types(
            (self.id, str),
            (self.name, str),
            (self.common_name, Optional[str]),
            (self.abbrev, Optional[str]),
            (self.coords, Coords),
        )
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __eq__(self, other: Self):
        if not isinstance(other, self.__class__):
            raise TypeError('`Building`s can only be compared '
                            'with other `Building` instances.')
        return hash(self) == hash(other)
