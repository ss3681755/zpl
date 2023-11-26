import sys

from tokenizer import tokenize
from parser import parse
from code_generator import generate

if __name__ == '__main__':
    program = sys.argv[1] if len(sys.argv) > 1 else 'sample.zpl'
    with open(program) as f: source = f.read()

    tokens = tokenize(source)
    ast = parse(tokens)
    asm = generate(ast)
    with open('out.asm', 'w+') as f: f.write(asm)
