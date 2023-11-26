from tokenizer import tokenize
from parser import parse
from code_generator import generate
import sys

def sample(source):
    tokens = tokenize(source)
    ast = parse(tokens)
    for row in ast:
        print(row)

def read_program(program):
    with open(program) as f:
        source = f.read()
    # sample(source)
    source = source.split('\n')
    parsable_source = []
    for line in source:
        # skip empty lines
        if line.strip() == '': continue
        # skip comments
        if line.startswith('#'): continue
        tokens = line.split(' ')
        parsable_source.append(tokens)
    return parsable_source

if __name__ == '__main__':
    program = sys.argv[1] if len(sys.argv) > 1 else 'sample.zpl'
    asm = generate(read_program(program))
    with open('out.asm', 'w+') as f:
        f.write(asm)
