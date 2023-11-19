import os, subprocess
from code_generator import generate

for file in os.listdir('tests'):
    if file.endswith('.zpl'):
        test_file = f"tests/{file}"
        output_file = test_file.replace('zpl', 'out')
        stdout, _ = subprocess.Popen(['make', '-B', test_file], stdout=subprocess.PIPE).communicate()
        with open('test.out', 'w+') as f2:
            f2.write(str(stdout.decode('ascii')))
        success = os.system(f'diff {output_file} test.out -u') == 0
        if not success: exit(1)
        else: os.system('make clean')
