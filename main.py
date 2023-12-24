import sys

from zpl import assemble

if __name__ == '__main__':
    program = sys.argv[1] if len(sys.argv) > 1 else 'sample.zpl'
    with open(program) as f: source = f.read()
    with open('out.asm', 'w+') as f: f.write(assemble(source))
