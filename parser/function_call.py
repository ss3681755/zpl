from .argument import parse_argument_list
from .terminals import parse_atom

def parse_function_call(cursor):
    fname = cursor.attempt(parse_atom)
    if fname is None: return

    arguments = cursor.attempt(parse_argument_list)
    if arguments is None: return

    return {'name': fname, 'arguments': arguments}