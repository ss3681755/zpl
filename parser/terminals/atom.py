from tokens import TokenType

def _parse_underscores(cursor):
    while cursor.can_move() and cursor.peek().token_type == TokenType.UNDERSCORE:
        cursor.move()

def _parse_alphabets(cursor):
    while cursor.can_move() and cursor.peek().token_type == TokenType.ALPHA:
        cursor.move()

# an atom is valid placeholder with regex [_a-zA-Z]+
def parse_atom(cursor):
    name = []
    while cursor.can_move():
        if underscores := cursor.attempt(_parse_underscores):
            name.extend(underscores)
        elif alphabets := cursor.attempt(_parse_alphabets):
            name.extend(alphabets)
        else:
            break

    return ''.join(map(lambda x: x.value, name))