from tokenizer import Cursor, TokenType, tokenize

def _join_tokens(tokens):
    return ''.join(map(lambda t: t.value, tokens)) or None

def _consume_token_of_type(cursor, token_type):
    while cursor.can_advance() and cursor.peek().token_type == token_type:
        cursor.advance()

def _consume(cursor, token_type):
    value = cursor.try_advance(lambda c: _consume_token_of_type(c, token_type))
    if value: return _join_tokens(value)

def _consume_one_token_of_type(cursor, token_type):
    if cursor.can_advance() and cursor.peek().token_type == token_type:
        cursor.advance()

def _consume_once(cursor, token_type):
    value = cursor.try_advance(lambda c: _consume_one_token_of_type(c, token_type))
    if value and len(value) == 1: return _join_tokens(value)

def _consume_empty_lines(cursor):
    spaces = _consume(cursor, TokenType.SPACE) or ''
    newlines = _consume(cursor, TokenType.NEWLINE) or ''
    while cursor.can_advance() and (len(spaces) > 0 or len(newlines) > 0):
        spaces = _consume(cursor, TokenType.SPACE) or ''
        newlines = _consume_once(cursor, TokenType.NEWLINE) or ''

def parse_sign(cursor):
    return _consume_once(cursor, TokenType.MINUS)

def parse_unsigned_literal(cursor):
    return _consume_once(cursor, TokenType.INTEGER)

def parse_signed_literal(cursor):
    sign = cursor.try_advance(parse_sign)
    if sign is None: return
    value = cursor.try_advance(parse_unsigned_literal)
    if value is None: return
    return sign + value

def parse_literal(cursor):
    signed_literal = cursor.try_advance(parse_signed_literal)
    if signed_literal is not None: return signed_literal

    unsigned_literal = cursor.try_advance(parse_unsigned_literal)
    if unsigned_literal is not None: return unsigned_literal

# an atom is valid placeholder with regex [_a-zA-Z]+
def parse_atom(cursor):
    name = []
    while cursor.can_advance():
        if underscores := _consume(cursor, TokenType.UNDERSCORE):
            name.append(underscores)

        if alphabets := _consume_once(cursor, TokenType.ALPHA):
            name.append(alphabets)

        if underscores is None and alphabets is None:
            break
    return ''.join(name) or None

def parse_argument(cursor):
    if atom := cursor.try_advance(parse_atom):
        return {'value': atom, 'type': 'atom'}

    if literal := cursor.try_advance(parse_literal):
        return {'value': literal, 'type': 'literal'}

def parse_function_call(cursor):
    fname = cursor.try_advance(parse_atom)
    if fname is None: return

    arguments = []
    while cursor.can_advance():
        # ignore spaces if any but there must be at least 1 space
        # if not that means we have reached the end of function call.
        if _consume(cursor, TokenType.SPACE) is None: break

        arg = cursor.try_advance(parse_argument)
        if arg is None: break
        arguments.append(arg)

    if len(arguments) == 0: return

    return {'name': fname, 'arguments': arguments}

def parse(tokens):
    nodes = []
    cursor = Cursor(tokens)
    _consume_empty_lines(cursor)
    while cursor.can_advance():
        if fn_call := cursor.try_advance(parse_function_call):
            nodes.append(fn_call)
        _consume_empty_lines(cursor)
    return nodes

with open('sample.zpl') as f:
    source = f.read()

def print_tokens(index):
    for t in tokens[:index]:
        print(t)

tokens = tokenize(source)
calls = parse(tokens)
for c in calls:
    args = ' '.join(map(lambda x: str(x['value']), c['arguments']))
    # print(args)
    print(c['name'], args)