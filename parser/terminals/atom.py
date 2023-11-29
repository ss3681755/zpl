from tokens import TokenType

def _parse_underscores(cursor):
    while cursor.can_move() and cursor.peek().token_type == TokenType.UNDERSCORE:
        cursor.move()

def _join_underscores(cursor):
    if tokens := cursor.attempt(_parse_underscores):
        return ''.join([t.value for t in tokens])

def _parse_alphabets(cursor):
    while cursor.can_move() and cursor.peek().token_type == TokenType.ALPHA:
        cursor.move()

def _join_alphabets(cursor):
    if tokens := cursor.attempt(_parse_alphabets):
        return ''.join([t.value for t in tokens])

# an atom is valid placeholder with regex [_a-zA-Z]+
def parse_atom(cursor):
    name = []
    while cursor.can_move():
        if underscores := cursor.attempt(_join_underscores):
            name.append(underscores)

        if alphabets := cursor.attempt(_join_alphabets):
            name.append(alphabets)

        if underscores is None and alphabets is None: break
    return ''.join(name) or None