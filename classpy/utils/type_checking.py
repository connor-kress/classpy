import typing


def check_types(*pairs: tuple[object, type]) -> None:
    """Checks that each pair of (object, type) matches correctly
    similarly to `isinstance(...)`.
    Raises `TypeError` if any pairs do not match.
    """
    for obj, type_ in pairs:
        if not isinstance(type_, type) and\
           not isinstance(type_, typing._UnionGenericAlias):
            raise TypeError(f'`{(type_.__class__)}` is not a `type`.')
        if not isinstance(obj, type_):
            type_name: str
            if isinstance(type_, type):
                type_name = type_.__name__
            else:
                type_name = repr(type_).removeprefix('typing.')
            raise TypeError(f'`{obj.__class__.__name__}` object is not '
                            f'of the expected type `{type_name}`.')
