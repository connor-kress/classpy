from typing import Optional
import regex as re

from ..course_req import CourseReq

from ..utils import (
    BooleanExpr,
    BooleanToken,
    BooleanAnd,
    BooleanOr,
)

AND = 'and'
OR = 'or'
LEFT_P = '('
RIGHT_P = ')'
ALL_TOKENS = (AND, OR, LEFT_P, RIGHT_P)

REMOVABLE_TERMS = (
    '.', ',', ';', ':',
    'with a minimum grade of C',
    'with minimum grades of C',
    'minimum grade of C',
)

CC_FIRST = re.compile(r'\b[A-Za-z]{3}\b')
CC_WHOLE = re.compile(r'\b[A-Za-z]{3}\W?\d{4}[A-Za-z]?\b')


def _tokenize(req_str: str) -> list[str]:
    words: list[str] = req_str.replace('(', ' ( ').replace(')', ' ) ').split()
    tokens: list[str] = []
    acc = ''
    while words:
        current = words.pop(0)
        if CC_FIRST.search(current) and words and CC_WHOLE.search(current + words[0]):
            if acc:
                tokens.append(acc)
                acc = ''
            tokens.append(current + words.pop(0))
        elif current in ALL_TOKENS or CC_WHOLE.search(current):
            if acc:
                tokens.append(acc)
                acc = ''
            tokens.append(current)
        else:
            acc = f'{acc} {current}' if acc else current
    if acc:
        tokens.append(acc)
        acc = ''
    return tokens


def _parse_expr_from_tokens(tokens: list[str]) -> BooleanExpr:
    def get_closing_index(starting_index: int) -> int:
        p_count = 1
        for i, token in enumerate(tokens[starting_index+1:]):
            if token == LEFT_P:
                p_count += 1
            elif token == RIGHT_P:
                p_count -= 1
                if p_count == 0:
                    return starting_index + i + 1
        raise ValueError('Unclosed parenthesis.')

    group_type: Optional[BooleanExpr] = None
    group: list[BooleanExpr] = []
    ready_for_term = True
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == LEFT_P:
            if not ready_for_term:
                raise ValueError('Invalid syntax. 1')
            closing_index = get_closing_index(i)
            group.append(_parse_expr_from_tokens(tokens[i+1:closing_index]))
            i = closing_index
            ready_for_term = False
        elif token == RIGHT_P:
            raise ValueError('Unbalanced parentheses.')
        elif token == OR or token == AND:
            if ready_for_term:
                raise ValueError('Invalid syntax. 2')
            elif group_type is None:
                group_type = token
                ready_for_term = True
            elif group_type != token:
                raise ValueError('Invalid syntax. 3')
            else:
                ready_for_term = True
        else:
            if isinstance(token, str):
                group.append(BooleanToken(token))
            elif isinstance(token, BooleanExpr):
                group.append(token)
            else:
                raise ValueError('Unexpected token type.')
            ready_for_term = False
        i += 1
    if group_type is None and len(group) > 1:
        raise ValueError('Invalid Syntax. 4')
    expr: BooleanExpr
    match group_type:
        case 'and': expr = BooleanAnd(*group)
        case 'or': expr = BooleanOr(*group)
        case None: expr = group[0]
    return expr


def parse_course_reqs(req_str: str) -> CourseReq:
    cleaned_str = req_str[:]
    for term in REMOVABLE_TERMS:
        cleaned_str = cleaned_str.replace(term, '')
    if not CC_WHOLE.search(cleaned_str):
        return CourseReq(req_str, None, None, None)
    tokens = _tokenize(cleaned_str)
    extra_and = None
    extra_or = None
    if len(tokens) > 2 and tokens[-2] == AND\
                       and not CC_WHOLE.search(tokens[-1]):
        extra_and = tokens[-1]
        tokens = tokens[:-2]
    elif len(tokens) > 2 and tokens[-2] == OR\
                         and not CC_WHOLE.search(tokens[-1]):
        extra_or = tokens[-1]
        tokens = tokens[:-2]
    if any(token not in ALL_TOKENS
           and not CC_WHOLE.search(token)
           for token in tokens):
        return CourseReq(req_str, None, None, None)
    try:
        boolean_expr = _parse_expr_from_tokens(tokens)
    except ValueError as e:
        # print(f'Error: {e}')
        return CourseReq(req_str, None, None, None)
    return CourseReq(req_str, boolean_expr, extra_and, extra_or)
