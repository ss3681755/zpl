from .tokenizer import tokenize
from .parser import parse
from .codegen import generate

def assemble(source):
    tokens = tokenize(source)
    ast = parse(tokens)
    return generate(ast)