from dataclasses import dataclass, field

from parser.argument import Argument, ArgumentType

# Stores the result of the last instruction
_PREV_RESULT = Argument('_', ArgumentType.ATOM)

@dataclass
class Scope:
    args: dict[Argument, int] = field(default_factory=dict)
    stack: int = field(default=0)

    def __getitem__(self, arg):
        match arg.kind:
            case ArgumentType.LITERAL:
                return arg
            case ArgumentType.ATOM:
                return f"QWORD [rsp+{8*(self.stack - self.args[arg] - 1)}]"
            case _:
                raise Exception(f'Unknown argument type {arg}')

    def __setitem__(self, arg, value):
        match arg.kind:
            case ArgumentType.LITERAL:
                raise Exception(f'Operation unsupported for {arg}')
            case ArgumentType.ATOM:
                self.args[arg] = value
            case _:
                raise Exception(f'Unknown argument type {arg}')

    def increment(self):
        self.args[_PREV_RESULT] = self.stack
        self.stack += 1

    # Clean up prev results if any.
    def clear(self):
        if _PREV_RESULT in self.args:
            del self.args[_PREV_RESULT]