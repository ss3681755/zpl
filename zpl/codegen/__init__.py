from .scope import Scope

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
        # [add, <int | variable>, <int | variable>]
        elif c.name == 'add':
            assert c.argcount == 2
            code.append(f"mov rax, {scope[c.args[0]]}")
            code.append(f"mov rdi, {scope[c.args[1]]}")
            code.append(f"add rax, rdi")
            code.append("push rax")
            scope.increment()
        # [sub, <int | variable>, <int | variable>]
        elif c.name == 'sub':
            assert c.argcount == 2
            code.append(f"mov rax, {scope[c.args[0]]}")
            code.append(f"mov rdi, {scope[c.args[1]]}")
            code.append(f"sub rax, rdi")
            code.append("push rax")
            scope.increment()
        # [and, <int | variable>, <int | variable>]
        elif c.name == 'and':
            assert c.argcount == 2
            code.append(f"mov rax, {scope[c.args[0]]}")
            code.append(f"mov rdi, {scope[c.args[1]]}")
            code.append(f"and rax, rdi")
            code.append("push rax")
            scope.increment()
        # [or, <int | variable>, <int | variable>]
        elif c.name == 'or':
            assert c.argcount == 2
            code.append(f"mov rax, {scope[c.args[0]]}")
            code.append(f"mov rdi, {scope[c.args[1]]}")
            code.append(f"or rax, rdi")
            code.append("push rax")
            scope.increment()
        # [xor, <int | variable>, <int | variable>]
        elif c.name == 'xor':
            assert c.argcount == 2
            code.append(f"mov rax, {scope[c.args[0]]}")
            code.append(f"mov rdi, {scope[c.args[1]]}")
            code.append(f"xor rax, rdi")
            code.append("push rax")
            scope.increment()
        # [inc, <int | variable>]
        elif c.name == 'inc':
            assert c.argcount == 1
            code.append(f"mov rax, {scope[c.args[0]]}")
            code.append(f"inc rax")
            code.append("push rax")
            scope.increment()
        # [dec, <int | variable>]
        elif c.name == 'dec':
            assert c.argcount == 1
            code.append(f"mov rax, {scope[c.args[0]]}")
            code.append(f"dec rax")
            code.append("push rax")
            scope.increment()
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
            assert c.argcount == 1
            arg1 = c.args[0]
            code.append(f"; -- print {arg1} to console --")
            code.append(f"mov rdi, {scope[arg1]}")
            code.append(f"call _print")
            # system calls do not have any output
            scope.clear()
        elif c.name == 'exit':
            assert c.argcount == 1
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