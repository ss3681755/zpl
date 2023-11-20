from code_generator import generate
import sys

def read_program(program):
    with open(program) as f:
        lines = f.read().strip().split('\n')
        return list(map(lambda x: x.strip().split(), lines))

if __name__ == '__main__':
    program = sys.argv[1] if len(sys.argv) > 1 else 'sample.zpl'
    asm = generate(read_program(program))
    with open('out.asm', 'w+') as f:
        f.write(asm)
