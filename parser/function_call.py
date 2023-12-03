from dataclasses import dataclass

from .argument import Argument, parse_argument_list
from .terminals import parse_atom

@dataclass
class FunctionCall:
    name: str
    args: list[Argument]

    def argcount(self):
        return len(self.args)

def parse_function_call(cursor):
    fname = cursor.attempt(parse_atom)
    if fname is None: return

    arguments = cursor.attempt(parse_argument_list)
    if arguments is None: return

    return FunctionCall(fname, arguments)