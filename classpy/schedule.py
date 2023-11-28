from typing import Optional, Literal

from .data import (
    WEEK_DAYS,
    FALL_SPRING_PERIODS,
    SUMMER_PERIODS,
)
from .locations import Coords, distance
from .class_ import Class

type CoordData = list[list[Optional[Coords]]]
type TermType = Literal['Fall', 'Spring', 'Summer']


def _get_coord_data(class_: Class) -> CoordData:
    return [
        [None if classroom is None else classroom.building.coords
            for classroom in day]
        for day in class_.locations
    ]


class Schedule:
    def __init__(self, term_type: TermType = 'Fall') -> None:
        """Instantiates a blank schedule with a size corresponding
        to the `term_type`.
        """
        if term_type in {'Fall', 'Spring'}:
            periods = FALL_SPRING_PERIODS
        elif term_type == 'Summer':
            periods = SUMMER_PERIODS
        else:
            raise ValueError(f'No such term type "{term_type}" exists.')
        self.data: CoordData = [
            [None for _ in range(periods)]
            for _ in range(WEEK_DAYS)
        ]

    def fits(self, class_: Class) -> bool:
        """Returns `True` if the passed `Class` fits in the
        `Schedule`, else `False`.
        """
        data = _get_coord_data(class_)
        assert len(data) == len(self.data)
        assert len(data[0]) == len(self.data[0])
        for day1, day2 in zip(self.data, data):
            for coords1, coords2 in zip(day1, day2):
                if coords1 is not None and coords2 is not None:
                    return False
        return True

    def add(self, class_: Class) -> None:
        """Adds the passed `Class`'s location data to the `Schedule`."""
        assert self.fits(class_)
        data = _get_coord_data(class_)
        for i, day in enumerate(data):
            for j, coords in enumerate(day):
                if coords is not None:
                    self.data[i][j] = coords

    def total_distance(self) -> float:
        """Returns the total distance between classes throughout the week."""
        acc = 0.0
        for day in self.data:
            current: Optional[Coords] = None
            for coords in day:
                if coords is None or coords == current:
                    continue
                if current is not None:
                    acc += distance(current, coords)
                current = coords
        return acc
