from cursor import Cursor

from terminals import parse_empty_lines, parse_single_line_comment
from .function_call import parse_function_call

def parse(tokens):
    nodes = []
    cursor = Cursor(tokens)
    while cursor.can_move():
        cursor.attempt(parse_empty_lines)
        cursor.attempt(parse_single_line_comment)
        if fn_call := cursor.attempt(parse_function_call):
            nodes.append(fn_call)
    return nodes