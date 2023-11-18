from .data import *
from .locations import *
from .parsing import *
from .scraping import *
from .utils import *

from .course import Course
from .course_req import CourseReq
from .class_ import Class
from .textbook import Textbook
from .textbook_info import TextbookInfo

from .class_functions import (
    add_class_course_binding,
    get_course_of,
)

__all__ = (
    *data.__all__ ,
    *locations.__all__,
    *parsing.__all__,
    *scraping.__all__ ,
    *utils.__all__ ,

    'Course',
    'CourseReq',
    'Class',
    'Textbook',
    'TextbookInfo',

    'add_class_course_binding',
    'get_course_of',
)
