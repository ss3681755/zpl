from tokenizer import Cursor, TokenType, tokenize

def join_tokens(tokens):
    return ''.join(map(lambda t: t.value, tokens)) or None

def consume_token_of_type(cursor, token_type):
    while cursor.can_advance() and cursor.peek().token_type == token_type:
        cursor.advance()

    if value := cursor.extract():
        return join_tokens(value)

def consume_spaces(cursor):
    return cursor.try_advance(lambda c: consume_token_of_type(c, TokenType.SPACE))

def consume_newlines(cursor):
    return cursor.try_advance(lambda c: consume_token_of_type(c, TokenType.NEWLINE))

def consume_underscores(cursor):
    return cursor.try_advance(lambda c: consume_token_of_type(c, TokenType.UNDERSCORE))

def consume_alphabets(cursor):
    return cursor.try_advance(lambda c: consume_token_of_type(c, TokenType.ALPHA))

def parse_unsigned_literal(cursor):
    if cursor.peek().token_type == TokenType.INTEGER:
        value = cursor.peek().value
        cursor.advance()
        return value

def parse_signed_literal(cursor):
    if not cursor.can_advance(): return
    if cursor.peek().token_type != TokenType.MINUS: return
    sign = cursor.peek().value
    cursor.advance() # move past sign
    literal = cursor.try_advance(parse_unsigned_literal)
    if literal is None: return
    return sign + literal

def parse_literal(cursor):
    signed_literal = parse_signed_literal(cursor)
    if signed_literal is not None: return signed_literal

    unsigned_literal = parse_unsigned_literal(cursor)
    if unsigned_literal is not None:
        return unsigned_literal

# an atom is valid placeholder with regex [_a-zA-Z]+
def parse_atom(cursor):
    name = []
    while cursor.can_advance():
        prev_length = len(name)
        underscores = consume_underscores(cursor)
        if underscores is not None: name.append(underscores)

        alphabets = consume_alphabets(cursor)
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

    spaces = consume_spaces(cursor)
    if spaces is None: return

    arguments = []
    while cursor.can_advance():
        arg = parse_argument(cursor)
        if arg is None: break

        arguments.append(arg)
        _ = consume_spaces(cursor)

    if len(arguments) == 0: return

    newlines = consume_newlines(cursor)
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