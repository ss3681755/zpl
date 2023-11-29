from tokens import TokenType

from .terminals import parse_atom, parse_literal

def _parse_spaces(cursor):
    while cursor.can_move() and cursor.peek().token_type == TokenType.SPACE:
        cursor.move()

def _count_spaces(cursor):
    if spaces := cursor.attempt(_parse_spaces):
        return len(spaces)
    return 0

def _parse_argument(cursor):
    if atom := cursor.attempt(parse_atom):
        return {'value': atom, 'type': 'atom'}

    if literal := cursor.attempt(parse_literal):
        return {'value': literal, 'type': 'literal'}

def parse_argument_list(cursor):
    arguments = []
    while cursor.can_move():
        # ignore spaces if any but there must be at least 1 space
        # if not that means we have reached the end of function call.
        if cursor.attempt(_count_spaces) == 0: break

        if arg := cursor.attempt(_parse_argument):
            arguments.append(arg)

    return arguments or None