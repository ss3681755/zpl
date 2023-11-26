from tokenizer import tokenize
from cursor import Cursor
from tokens import TokenType

def _join_tokens(tokens):
    return ''.join(map(lambda t: t.value, tokens)) or None

def _parse_token_of_type(cursor, token_type):
    while cursor.can_move() and cursor.peek().token_type == token_type:
        cursor.move()

def _parse(cursor, token_type):
    value = cursor.attempt(lambda c: _parse_token_of_type(c, token_type))
    if value: return _join_tokens(value)

def _parse_one_token_of_type(cursor, token_type):
    if cursor.can_move() and cursor.peek().token_type == token_type:
        cursor.move()

def _parse_once(cursor, token_type):
    value = cursor.attempt(lambda c: _parse_one_token_of_type(c, token_type))
    if value and len(value) == 1: return _join_tokens(value)

def _parse_empty_lines(cursor):
    spaces = _parse(cursor, TokenType.SPACE) or ''
    newlines = _parse(cursor, TokenType.NEWLINE) or ''
    while cursor.can_move() and (len(spaces) > 0 or len(newlines) > 0):
        spaces = _parse(cursor, TokenType.SPACE) or ''
        newlines = _parse_once(cursor, TokenType.NEWLINE) or ''

def _parse_single_line_comment(cursor):
    _hash = _parse_once(cursor, TokenType.HASH)
    if _hash is None: return
    while cursor.can_move() and cursor.peek().token_type != TokenType.NEWLINE:
        cursor.move()

def parse_sign(cursor):
    return _parse_once(cursor, TokenType.MINUS)

def parse_unsigned_literal(cursor):
    return _parse_once(cursor, TokenType.INTEGER)

def parse_signed_literal(cursor):
    sign = cursor.attempt(parse_sign)
    if sign is None: return
    value = cursor.attempt(parse_unsigned_literal)
    if value is None: return
    return sign + value

def parse_literal(cursor):
    signed_literal = cursor.attempt(parse_signed_literal)
    if signed_literal is not None: return signed_literal

    unsigned_literal = cursor.attempt(parse_unsigned_literal)
    if unsigned_literal is not None: return unsigned_literal

# an atom is valid placeholder with regex [_a-zA-Z]+
def parse_atom(cursor):
    name = []
    while cursor.can_move():
        if underscores := _parse(cursor, TokenType.UNDERSCORE):
            name.append(underscores)

        if alphabets := _parse_once(cursor, TokenType.ALPHA):
            name.append(alphabets)

        if underscores is None and alphabets is None:
            break
    return ''.join(name) or None

def parse_argument(cursor):
    if atom := cursor.attempt(parse_atom):
        return {'value': atom, 'type': 'atom'}

    if literal := cursor.attempt(parse_literal):
        return {'value': literal, 'type': 'literal'}

def parse_argument_list(cursor):
    arguments = []
    while cursor.can_move():
        # ignore spaces if any but there must be at least 1 space
        # if not that means we have reached the end of function call.
        if _parse(cursor, TokenType.SPACE) is None: break

        arg = cursor.attempt(parse_argument)
        if arg is None: break
        arguments.append(arg)

    if len(arguments) > 0: return arguments

def parse_function_call(cursor):
    fname = cursor.attempt(parse_atom)
    if fname is None: return

    arguments = cursor.attempt(parse_argument_list)
    if arguments is None: return

    return {'name': fname, 'arguments': arguments}

def parse(tokens):
    nodes = []
    cursor = Cursor(tokens)
    _parse_empty_lines(cursor)
    while cursor.can_move():
        if fn_call := cursor.attempt(parse_function_call):
            nodes.append(fn_call)
        _parse_empty_lines(cursor)
        _parse_single_line_comment(cursor)
    return nodes