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
    signed_literal = cursor.attempt(_parse_signed_literal)
    if signed_literal is not None: return signed_literal

    unsigned_literal = cursor.attempt(_parse_unsigned_literal)
    if unsigned_literal is not None: return unsigned_literal