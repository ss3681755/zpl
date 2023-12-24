from .scope import Scope

X86_64_REGISTERS = ['rax', 'rdi', 'rsi', 'rdx', 'r10', 'r8', 'r9']
ARITY_2_FUNCTIONS = ['add', 'sub', 'and', 'or', 'xor']
ARITY_1_FUNCTIONS = ['inc', 'dec']

def make_name_call(scope, fn, args):
    assert len(args) <= len(X86_64_REGISTERS), f"name only support params upto {len(X86_64_REGISTERS)}."

    code = [f"; -- call {fn} with params {' '.join(map(str, args))} --"]
    for reg, arg in zip(X86_64_REGISTERS, args):
        code.append(f"mov {reg}, {scope[arg]}")

    code.append(f"{fn} {', '.join(X86_64_REGISTERS[:len(args)])}")
    code.append("push rax")
    scope.increment()
    return code

def generate(calls):
    code = [
        'section .text',
        'global _start',
        'extern _print',
        'extern _exit',
        '; -- entrypoint --',
        '_start:',
    ]
    scope = Scope()
    index = 0
    while index < len(calls):
        c = calls[index]
        # ['assign', str variable name, int literal | str variable ref]
        if c.name == 'assign':
            arg1, arg2 = c.args
            code.append(f"; -- {arg1} = {arg2} --")
            code.append(f"push {scope[arg2]}")

            scope[arg1] = scope.stack
            scope.increment()
        # [<fn>, <int | variable>, <int | variable>]
        elif c.name in ARITY_2_FUNCTIONS:
            assert c.argcount() == 2
            code.extend(make_name_call(scope, c.name, c.args))
        # [<fn>, <int | variable>]
        elif c.name in ARITY_1_FUNCTIONS:
            assert c.argcount() == 1
            code.extend(make_name_call(scope, c.name, c.args))
        elif c.name == 'div':
            arg1, arg2 = c.args
            # find a way to handle divide by 0 error before generating the asm
            code.append(f"; -- call {c.name} with params {' '.join(map(str, c.args))} --")
            code.append("xor rdx, rdx")
            code.append(f"mov rax, {scope[arg1]}")
            code.append(f"mov rdi, {scope[arg2]}")
            code.append(f"div rdi")
            code.append("push rax")
            scope.increment()
        elif c.name == 'rem':
            arg1, arg2 = c.args
            # find a way to handle divide by 0 error before generating the asm
            code.append(f"; -- call {c.name} with params {' '.join(map(str, c.args))} --")
            code.append("xor rdx, rdx")
            code.append(f"mov rax, {scope[arg1]}")
            code.append(f"mov rdi, {scope[arg2]}")
            code.append(f"div rdi")
            code.append("push rdx")
            scope.increment()
        elif c.name == 'mul':
            arg1, arg2 = c.args
            code.append(f"; -- call {c.name} with params {' '.join(map(str, c.args))} --")
            code.append(f"mov rax, {scope[arg1]}")
            code.append(f"mov rdi, {scope[arg2]}")
            code.append(f"mul rdi")
            code.append("push rax")
            scope.increment()
        # ['print', int literal | str variable ref]
        elif c.name == 'print':
            assert c.argcount() == 1
            arg1 = c.args[0]
            code.append(f"; -- print {arg1} to console --")
            code.append(f"mov rdi, {scope[arg1]}")
            code.append(f"call _print")
            # system calls do not have any output
            scope.clear()
        elif c.name == 'exit':
            assert c.argcount() == 1
            arg1 = c.args[0]
            code.append(f"; -- exit with code {arg1} --")
            code.append(f"mov rdi, {scope[arg1]}")
            code.append(f"call _exit")
            # system calls do not have any output
            scope.clear()
        else:
            raise Exception(f'Unknow name call {" ".join(map(str, c))}')
        index += 1
    return '\n'.join(code)