import os, subprocess
from code_generator import generate

def test_command(test_file, output_file):
    return f'make PROGRAM={test_file} OUTPUT={output_file} verify'

for file in os.listdir('tests'):
    if file.endswith('.zpl'):
        test_file = f"tests/{file}"
        output_file = test_file.replace('zpl', 'out')
        command = test_command(test_file, output_file)
        result = os.system(command)
        if result == 0: os.system('make clean')
        else: exit(1)
