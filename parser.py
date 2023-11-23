from tokenizer import Cursor, TokenType, tokenize

def join_tokens(tokens, start, end):
    return ''.join(map(lambda t: t.value, tokens[start:end])) or None

def consume_token_of_type(index, tokens, token_type):
    start = index
    while index < len(tokens) and tokens[index].token_type == token_type:
        index += 1

    value = join_tokens(tokens, start, index)
    return (start, None) if value is None else (index, value)

def consume_spaces(index, tokens):
    return consume_token_of_type(index, tokens, TokenType.SPACE)

def consume_newlines(index, tokens):
    return consume_token_of_type(index, tokens, TokenType.NEWLINE)

def consume_underscores(index, tokens):
    return consume_token_of_type(index, tokens, TokenType.UNDERSCORE)

def consume_alphabets(index, tokens):
    return consume_token_of_type(index, tokens, TokenType.ALPHA)

def parse_signed_literal(index, tokens):
    if index == len(tokens): return index, None
    if tokens[index].token_type != TokenType.MINUS: return index, None
    start = index
    # skip MINUS token
    index += 1
    index, literal = parse_unsigned_literal(index, tokens)
    if literal is None: return start, None
    return index, -1 * literal

def parse_unsigned_literal(index, tokens):
    if index == len(tokens): return index, None
    # only +/- integer literals are supported for now.
    match tokens[index].token_type:
        case TokenType.INTEGER:
            return index + 1, int(tokens[index].value)
        case _:
            return index, None

def parse_literal(index, tokens):
    start = index
    index, signed_literal = parse_signed_literal(index, tokens)
    if signed_literal is not None:
        return index, signed_literal

    index, unsigned_literal = parse_unsigned_literal(index, tokens)
    if unsigned_literal is not None:
        return index, unsigned_literal

    return start, None

# an atom is valid placeholder with regex [_a-zA-Z]+
def parse_atom(index, tokens):
    name = []
    start = index
    while index < len(tokens):
        prev_length = len(name)
        index, underscores = consume_underscores(index, tokens)
        if underscores is not None: name.append(underscores)

        index, alphabets = consume_alphabets(index, tokens)
        if alphabets is not None: name.append(alphabets)
        # we neither found underscores nor alphabets
        if prev_length == len(name): break
    name = ''.join(name)
    if len(name) == 0:
        return start, None
    return index, name

def parse_argument(index, tokens):
    start = index
    argument = {}
    index, atom = parse_atom(index, tokens)
    if atom is not None:
        argument['value'] = atom
        argument['type'] = 'atom'
        return index, argument

    index, literal = parse_literal(index, tokens)
    if literal is not None:
        argument['value'] = literal
        argument['type'] = 'literal'
        return index, argument

    return start, None


def parse_function_call(index, tokens):
    start = index
    function = {}

    index, fname = parse_atom(index, tokens)
    if fname is None:
        return start, None
    function['name'] = fname

    index, spaces = consume_spaces(index, tokens)
    if spaces is None:
        return start, None

    arguments = []
    while index < len(tokens):
        index, arg = parse_argument(index, tokens)
        if arg is not None: arguments.append(arg)
        else: break

        index, _ = consume_spaces(index, tokens)

    if len(arguments) == 0:
        return start, None

    function['arguments'] = arguments
    index, newlines = consume_newlines(index, tokens)
    if newlines is None:
        return start, None

    return index, function

def parse(tokens):
    index = 0
    nodes = []
    cursor = Cursor(tokens)
    while index < len(tokens):
        index, node = parse_function_call(index, tokens)
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