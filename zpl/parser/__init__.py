from zpl.cursor import Cursor

from zpl.terminals import parse_empty_lines, parse_single_line_comment
from .function_call import parse_function_call

def parse(tokens):
    nodes = []
    cursor = Cursor(tokens)
    while cursor.can_move():
        if fn_call := cursor.attempt(parse_function_call):
            nodes.append(fn_call)
        elif _ := cursor.attempt(parse_empty_lines):
            pass
        elif _ := cursor.attempt(parse_single_line_comment):
            pass
        else:
            break
    return nodes