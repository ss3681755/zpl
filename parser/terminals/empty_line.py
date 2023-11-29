from tokens import TokenType

def _parse_spaces(cursor):
    while cursor.can_move() and cursor.peek().token_type == TokenType.SPACE:
        cursor.move()

def _parse_newlines(cursor):
    while cursor.can_move() and cursor.peek().token_type == TokenType.NEWLINE:
        cursor.move()

def _count_spaces(cursor):
    if spaces := cursor.attempt(_parse_spaces):
        return len(spaces)
    return 0

def _count_newlines(cursor):
    if newlines := cursor.attempt(_parse_newlines):
        return len(newlines)
    return 0

def parse_empty_lines(cursor):
    spaces = cursor.attempt(_count_spaces)
    newlines = cursor.attempt(_count_newlines)
    while cursor.can_move() and (spaces > 0 or newlines > 0):
        spaces = cursor.attempt(_count_spaces)
        newlines = cursor.attempt(_count_newlines)