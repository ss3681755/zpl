from tokens import TokenType

def _parse_hash(cursor):
    if cursor.can_move() and cursor.peek().token_type == TokenType.HASH:
        cursor.move()

def parse_single_line_comment(cursor):
    hash_ = cursor.attempt(_parse_hash)
    if hash_ is None: return
    while cursor.can_move() and cursor.peek().token_type != TokenType.NEWLINE:
        cursor.move()
