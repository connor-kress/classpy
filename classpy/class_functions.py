from .course import Course
from .class_ import Class

CLASS_COURSE_DICT = dict[Class, Course]()


def add_class_course_binding(class_: Class, course: Course) -> None:
    """Adds binding in the global `CLASS_COURSE_DICT` variable
    between `Class`es and `Course`s to make the `get_course_of(...)`
    function work.
    """
    CLASS_COURSE_DICT[class_] = course


def get_course_of(class_: Class) -> Course:
    """Attempts to retrieve the `Course` that the passed `Class` instance
    belongs to (used in conjunction with `add_class_course_binding(...)`).
    """
    if class_ not in CLASS_COURSE_DICT:
        raise Exception(f'Class ({class_.number}) not in `CLASS_COURSE_DICT`.')
    return CLASS_COURSE_DICT[class_]
