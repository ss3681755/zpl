import os, subprocess, sys

def test_command(test_file, output_file):
    return f'make PROGRAM={test_file} OUTPUT={output_file} verify'

def validate_output(test_dir):
    for file in os.listdir(test_dir):
        if file.endswith('.zpl'):
            test_file = f"{test_dir}/{file}"
            output_file = test_file.replace('zpl', 'out')
            command = test_command(test_file, output_file)
            result = os.system(command)
            # test output validation failed
            if result != 0: exit(1)
    # cleanup if all tests passed.
    os.system('make clean')

if __name__ == '__main__':
    test_dir = sys.argv[1] if len(sys.argv) > 1 else 'tests'
    validate_output(test_dir)