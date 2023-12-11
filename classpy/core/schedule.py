from typing import Optional, Literal

from ..data import (
    WEEK_DAYS,
    FALL_SPRING_PERIODS,
    SUMMER_PERIODS,
    DEFAULT_TERM_TYPE,
    DAY_OF_WEEK_DICT,
    SCHEDULE_COLUMN_WIDTH,
)
from ..locations import Coords, distance, ClassRoom
from .class_ import Class

type ClassroomData = list[list[Optional[ClassRoom]]]
type CoordData = list[list[Optional[Coords]]]
type TermType = Literal['Fall', 'Spring', 'Summer']


def _get_coord_data(classroom_data: ClassroomData) -> CoordData:
    return [
        [None if classroom is None else classroom.building.coords
            for classroom in day]
        for day in classroom_data
    ]


class Schedule:
    def __init__(self, term_type: TermType = DEFAULT_TERM_TYPE) -> None:
        """Instantiates a blank schedule with a size corresponding
        to the `term_type`.
        """
        if term_type in {'Fall', 'Spring'}:
            periods = FALL_SPRING_PERIODS
        elif term_type == 'Summer':
            periods = SUMMER_PERIODS
        else:
            raise ValueError(f'No such term type "{term_type}" exists.')
        self.data: ClassroomData = [
            [None for _ in range(periods)]
            for _ in range(WEEK_DAYS)
        ]
    
    def __str__(self) -> str:
        def str_of_item(classroom: Optional[ClassRoom]) -> str:
            if classroom is not None:
                return classroom.code.center(SCHEDULE_COLUMN_WIDTH)
            else:
                return ' ' * SCHEDULE_COLUMN_WIDTH

        day_strs = tuple(DAY_OF_WEEK_DICT.keys())
        data: ClassroomData = tuple(zip(*self.data))
        divider = ' '*3 + '-'*((SCHEDULE_COLUMN_WIDTH+1)*len(day_strs)+1) + '\n'
        schedule_str = ' '*3 + f' {' '.join(day.center(SCHEDULE_COLUMN_WIDTH)
                                    for day in day_strs)} \n' + divider
        for i, periods in enumerate(data):
            schedule_str += f'{i+1:<2} |{'|'.join(str_of_item(period)
                                         for period in periods)}|\n' + divider
        return schedule_str.removesuffix('\n')

    def fits(self, class_: Class) -> bool:
        """Returns `True` if the passed `Class` fits in the
        `Schedule`, else `False`.
        """
        data = class_.locations
        assert len(data) == len(self.data)
        assert len(data[0]) == len(self.data[0])
        for day1, day2 in zip(self.data, data):
            for room1, room2 in zip(day1, day2):
                if room1 is not None and room2 is not None:
                    return False
        return True

    def add(self, class_: Class) -> None:
        """Adds the passed `Class`'s location data to the `Schedule`."""
        assert self.fits(class_)
        for i, day in enumerate(class_.locations):
            for j, room in enumerate(day):
                if room is not None:
                    self.data[i][j] = room

    def total_distance(self) -> float:
        """Returns the total distance between classes throughout the week."""
        coord_data = _get_coord_data(self.data)
        acc = 0.0
        for day in coord_data:
            current: Optional[Coords] = None
            for coords in day:
                if coords is None or coords == current:
                    continue
                if current is not None:
                    acc += distance(current, coords)
                current = coords
        return acc
