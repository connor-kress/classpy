from playwright.async_api import BrowserContext
from typing import Optional

from .data import (
    DEFAULT_TERM_TYPE,
    DAY_OF_WEEK_DICT,
)
from .class_functions import get_course_of
from .core.schedule import TermType
from .core import (
    Class,
    Course,
    Schedule,
)
from .scraping import course_query
from .utils import clear_screen


async def _make_query(ctx: BrowserContext) -> Optional[tuple[Course]]:
    while True:
        clear_screen()
        course_code = input('Course code (eg. "MAD2502"): ').strip() or None
        course_title = input('Course title (eg. "Calculus 2"): ').strip() or None
        clear_screen()
        results = await course_query(ctx, code=course_code, title=course_title)
        if results:
            clear_screen()
            return results
        print('No results found.\n'
                'Type "exit" to return, else hit enter to try another query.')
        if input('> ').strip() == 'exit':
            clear_screen()
            return None



def _get_course_selection(courses: tuple[Course]) -> Optional[Course]:
    if len(courses) == 1:
        return courses[0]
    selection = None
    print_error_msg = False
    while True:
        clear_screen()
        print(f'{len(courses)} results:')
        for i, course in enumerate(courses):
            print(f'\t{i+1}: {course.number} - {course.title}')
        if print_error_msg:
            print('Please make a valid selection.')
        try:
            input_ = input('Selection ("exit" to return): ').strip()
            if input_.lower() == 'exit':
                clear_screen()
                return None
            selection = int(input_) - 1
            if not 0 <= selection < len(courses):
                raise ValueError
            break
        except ValueError:
            print_error_msg = True
    clear_screen()
    return courses[selection]


class ScheduleBuider:
    def __init__(self, term_type: TermType = DEFAULT_TERM_TYPE) -> None:
        self.schedule = Schedule(term_type)
        self.classes = set[Class]()
    
    def _total_credits(self) -> int:
        """Returns the total number of credit hours of the current schedule."""
        return sum(get_course_of(class_).credits for class_ in self.classes)

    def _get_class_selection(self, course: Course) -> Optional[Class]:
        """Returns a user `Class` selection from a `Course`.
        Returns `None` if no class is chosen.
        """
        classes = course.available_classes
        available_classes = sum(self.schedule.fits(class_)
                                for class_ in classes)
        idx_to_class = dict[int, Class]()
        if available_classes == 1:
            classes_str = f'{available_classes} available class:\n'
        else:
            classes_str = f'{available_classes} available classes:\n'
        i = 1
        for class_ in classes:
            info = (class_.number or 'No class #', class_.type_,
                    class_.instructors[0] if class_.instructors else None)
            if self.schedule.fits(class_):
                idx = str(i)
                idx_to_class[i] = class_
                i += 1
            else:
                idx = 'x'
            classes_str += f'\t{idx}: {' - '.join(term for term in info
                                                  if term is not None)}\n'
        classes_str.removesuffix('\n')
        i -= 1
        if not available_classes:
            print(classes_str)
            print('Hit enter to exit.')
            input()
            clear_screen()
            return None
        selection = None
        print_error_msg = False
        while True:
            clear_screen()
            print(classes_str)
            if print_error_msg:
                print('Please make a valid selection.')
            try:
                input_ = input('Selection ("exit" to return): ').strip()
                if input_.lower() == 'exit':
                    clear_screen()
                    return None
                selection = int(input_)
                if not 1 <= selection <= i:
                    raise ValueError
                break
            except ValueError:
                print_error_msg = True
        clear_screen()
        return idx_to_class[selection]
        
    
    async def _query_class(self, ctx: BrowserContext) -> Optional[Class]:
        """Returns a user `Class` selection from the UF Schedule of Courses.
        Returns `None` if no class is chosen.
        """
        results = await _make_query(ctx)
        if results is None:
            return None
        class_ = None
        while True:
            course = _get_course_selection(results)
            if course is None:
                return None
            class_ = self._get_class_selection(course)
            if class_ is not None:
                return class_
    
    async def build(self, ctx: BrowserContext) -> Schedule:
        """Builds a `Schedule` using user terminal queries to the
        UF Schedule of Courses using the `course_query(...)` function.
        """
        while True:
            class_ = await self._query_class(ctx)
            if class_ is not None:
                self.schedule.add(class_)
                self.classes.add(class_)
            print(self.schedule)
            print(f'Total credits: {self._total_credits()}')
            if input('Type "exit" to exit, else hit enter: ')\
                .strip().lower() == 'exit':
                break
            clear_screen()
        clear_screen()
        return self.schedule
