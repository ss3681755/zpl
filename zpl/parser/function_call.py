from dataclasses import dataclass

from zpl.terminals import parse_atom
from .argument import Argument, parse_argument_list

@dataclass
class FunctionCall:
    name: str
    args: list[Argument]

    @property
    def argcount(self):
        return len(self.args)

    @property
    def description(self):
        str_args = ' '.join(map(str, self.args))
        return f"; -- call {self.name} with params {str_args} --"

def parse_function_call(cursor):
    fname = cursor.attempt(parse_atom)
    if fname is None: return

    arguments = cursor.attempt(parse_argument_list)
    if arguments is None: return

    return FunctionCall(fname, arguments)