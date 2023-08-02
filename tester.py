import os, subprocess
from code_generator import generate

for test_file in os.listdir('tests'):
    if test_file.endswith('.zpl'):
        expected_output_file = f"tests/{test_file.replace('.zpl', '.out')}"
        with open(f'tests/{test_file}') as f:
            program = [line.split() for line in f.read().split('\n') if line]
            asmcode = generate(program)
            with open('out.asm', 'w+') as f1:
                f1.write(asmcode)
            stdout, _ = subprocess.Popen(['make', 'run'], stdout=subprocess.PIPE).communicate()
            with open('test.out', 'w+') as f2:
                f2.write(str(stdout.decode('ascii')))
            success = os.system(f'diff {expected_output_file} test.out -u') == 0
            if not success:
                print(f'Test {test_file} failed.')
                exit(1)