class Cursor:
    def __init__(self, text):
        self.text = text
        self.index = 0
        self.line = 0
        self.offset = 0
        self.__checkpoints = []

    def extract(self):
        assert len(self.__checkpoints) > 0, 'Extraction is allowed only when checkpointed.'
        index = self.__checkpoints[-1][0]
        if self.index == index: return None
        return self.text[index:self.index]

    def can_advance(self):
        return self.index < len(self.text)

    def peek(self):
        assert self.can_advance()
        return self.text[self.index]

    def advance(self):
        assert self.can_advance()
        if self.text[self.index] == '\n':
            self.line += 1
            self.offset = 1
        self.index += 1

    def try_advance(self, callback):
        if not self.can_advance(): return
        self.__checkpoint()
        value = callback(self)
        if value is None: self.__reset()
        else: self.__commit()
        return value

    def __checkpoint(self):
        self.__checkpoints.append((self.index, self.line, self.offset))

    def __reset(self):
        self.index, self.line, self.offset = self.__checkpoints.pop()

    def __commit(self):
        self.__checkpoints.pop()
