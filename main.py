from code_generator import generate

if __name__ == '__main__':
    code = generate(
        [
            ['assign', 'x', '10'],
            ['print', '20'],
            ['print', 'x'],
            ['assign', 'y', '30'],
            ['print', 'y'],
            ['assign', 'z', 'y'],
            ['print', 'z'],
            ['print', '-10'],
            ['assign', 'a', '-12'],
            ['print', 'a'],
            ['add', '5', '10'],
            ['print', '_'],
            ['add', 'x', '10'],
            ['print', '_'],
            ['add', '-5', 'x'],
            ['print', '_'],
            ['add', 'y', 'x'],
            ['print', '_'],
            ['sub', '5', '10'],
            ['print', '_'],
            ['sub', 'x', '10'],
            ['print', '_'],
            ['sub', '-5', 'x'],
            ['print', '_'],
            ['sub', 'y', 'x'],
            ['print', '_'],
            ['and', '10', '2'],
            ['print', '_'],
            ['and', 'x', 'y'],
            ['print', '_'],
            ['or', '10', '2'],
            ['print', '_'],
            ['or', 'x', 'y'],
            ['print', '_'],
            ['xor', '10', '2'],
            ['print', '_'],
            ['xor', 'x', 'y'],
            ['print', '_'],
            ['exit', '0'],
        ]
    )
    with open('out.asm', 'w+') as f:
        f.write(code)