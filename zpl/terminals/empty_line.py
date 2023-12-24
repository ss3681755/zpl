from zpl.tokens import TokenType

def _parse_spaces(cursor):
    while cursor.can_move() and cursor.peek().token_type == TokenType.SPACE:
        cursor.move()

def _parse_newlines(cursor):
    while cursor.can_move() and cursor.peek().token_type == TokenType.NEWLINE:
        cursor.move()

def parse_empty_lines(cursor):
    while cursor.can_move():
        if spaces := cursor.attempt(_parse_spaces): pass
        elif newlines := cursor.attempt(_parse_newlines): pass
        else: break
