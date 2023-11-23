class Cursor:
    def __init__(self, text):
        self.text = text
        self.index = self.__index = 0
        self.line = self.__line = 0
        self.offset = self.__offset = 0
        self.__locked = False

    def extract(self):
        assert self.__locked , 'Extract is allowed only when cursor is locked.'
        if self.index == self.__index: return None
        return self.text[self.index:self.__index]

    def can_advance(self):
        return self.__index < len(self.text)

    def peek(self):
        assert self.can_advance()
        return self.text[self.__index]

    def advance(self):
        assert self.can_advance()
        if self.text[self.__index] == '\n':
            self.__line += 1
            self.__offset = 1
        self.__index += 1

    def try_advance(self, callback):
        if not self.can_advance(): return
        self.__lock()
        value = callback(self)
        if value is None: self.__rollback()
        else: self.__commit()
        return value

    def __lock(self):
        assert not self.__locked, 'Cursor already locked.'
        self.__locked = True

    def __rollback(self):
        assert self.__locked, 'Rollback is allowed only when cursor is locked.'
        self.__index = self.index
        self.__line = self.line
        self.__offset = self.offset
        self.__locked = False

    def __commit(self):
        assert self.__locked, 'Commit is allowed only when cursor is locked.'
        self.index = self.__index
        self.line = self.__line
        self.offset = self.__offset
        self.__locked = False
