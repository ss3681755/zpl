from tokens import TokenType

def _parse_sign(cursor):
    if cursor.can_move() and cursor.peek().token_type == TokenType.MINUS:
        token = cursor.peek().value
        cursor.move()
        return token

def _parse_unsigned_literal(cursor):
    if cursor.can_move() and cursor.peek().token_type == TokenType.INTEGER:
        token = cursor.peek().value
        cursor.move()
        return token

def _parse_signed_literal(cursor):
    sign = cursor.attempt(_parse_sign)
    if sign is None: return

    literal = cursor.attempt(_parse_unsigned_literal)
    if literal is None: return

    return sign + literal

def parse_literal(cursor):
    if signed_literal := cursor.attempt(_parse_signed_literal):
        return signed_literal
    elif unsigned_literal := cursor.attempt(_parse_unsigned_literal):
        return unsigned_literal