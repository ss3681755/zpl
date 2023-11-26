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

def parse_sign(cursor):
    return _consume_once(cursor, TokenType.MINUS)

def parse_unsigned_literal(cursor):
    return _consume_once(cursor, TokenType.INTEGER)

def parse_signed_literal(cursor):
    sign = parse_sign(cursor)
    if value := parse_unsigned_literal(cursor):
        return (sign or '') + value

def parse_literal(cursor):
    if signed_literal := parse_signed_literal(cursor):
        return signed_literal

    if unsigned_literal := parse_unsigned_literal(cursor):
        return unsigned_literal

# an atom is valid placeholder with regex [_a-zA-Z]+
def parse_atom(cursor):
    name = []
    while cursor.can_advance():
        prev_length = len(name)
        underscores = _consume(cursor, TokenType.UNDERSCORE)
        if underscores is not None: name.append(underscores)

        alphabets = _consume_once(cursor, TokenType.ALPHA)
        if alphabets is not None: name.append(alphabets)
        # we neither found underscores nor alphabets
        if prev_length == len(name): break
    return ''.join(name) or None

def parse_argument(cursor):
    atom = parse_atom(cursor)
    if atom is not None:
        return {'value': atom, 'type': 'atom'}

    literal = parse_literal(cursor)
    if literal is not None:
        return {'value': literal, 'type': 'literal'}

def parse_function_call(cursor):
    fname = parse_atom(cursor)
    if fname is None: return

    spaces = _consume(cursor, TokenType.SPACE)
    if spaces is None: return

    arguments = []
    while cursor.can_advance():
        arg = parse_argument(cursor)
        if arg is None: break

        arguments.append(arg)
        _ = _consume(cursor, TokenType.SPACE)

    if len(arguments) == 0: return

    newlines = _consume(cursor, TokenType.NEWLINE)
    if newlines is None: return

    return {'name': fname, 'arguments': arguments}

def parse(tokens):
    nodes = []
    cursor = Cursor(tokens)
    while cursor.can_advance():
        node = parse_function_call(cursor)
        if node is None:
            return []
        nodes.append(node)
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