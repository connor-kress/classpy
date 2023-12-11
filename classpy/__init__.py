from .core import *
from .data import *
from .locations import *
from .parsing import *
from .scraping import *
from .utils import *

# this is to avoid some naming conflicts
from .locations import __all__\
    as locations__all__

from .class_functions import (
    add_class_course_binding,
    get_course_of,
)
from .gator_evals_searcher import gator_evals_searcher
from .schedule_builder import ScheduleBuider

__all__ = (
    *core.__all__,
    *data.__all__ ,
    *locations__all__,
    *parsing.__all__,
    *scraping.__all__ ,
    *utils.__all__ ,

    'add_class_course_binding',
    'get_course_of',
    'gator_evals_searcher',
    'ScheduleBuider',
)
