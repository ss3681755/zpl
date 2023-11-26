def tokenize(cursor):
    while cursor.can_move() and ord('0') <= ord(cursor.peek()) <= ord('9'):
        cursor.move()