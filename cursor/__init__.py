class Cursor:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.line = 0
        self.offset = 0
        self.__checkpoints = []

    def can_move(self):
        return self.index < len(self.text)

    def peek(self):
        assert self.can_move()
        return self.text[self.index]

    def move(self):
        assert self.can_move()
        if self.text[self.index] == '\n':
            self.line += 1
            self.offset = 1
        self.index += 1

    def attempt(self, callback):
        if not self.can_move(): return
        self.__checkpoint()
        value = callback(self)
        if value is None:
            value = self.__extract()
        if value is None:
            self.__reset()
            return
        self.__commit()
        return value

    def __checkpoint(self):
        self.__checkpoints.append((self.index, self.line, self.offset))

    def __reset(self):
        self.index, self.line, self.offset = self.__checkpoints.pop()

    def __commit(self):
        self.__checkpoints.pop()

    def __extract(self):
        index = self.__checkpoints[-1][0]
        if self.index == index: return None
        return self.text[index:self.index]