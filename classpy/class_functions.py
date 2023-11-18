from .course import Course
from .class_ import Class

CLASS_COURSE_DICT: dict[Class, Course] = {}


def add_class_course_binding(class_: Class, course: Course) -> None:
    CLASS_COURSE_DICT[class_] = course


def get_course_of(class_: Class) -> Course:
    if class_ not in CLASS_COURSE_DICT:
        raise Exception(f'Class ({class_.number}) not in `CLASS_COURSE_DICT`.')
    return CLASS_COURSE_DICT[class_]
