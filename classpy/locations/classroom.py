from dataclasses import dataclass

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
