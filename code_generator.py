X86_64_REGISTERS = ['rax', 'rdi', 'rsi', 'rdx', 'r10', 'r8', 'r9']
ARITY_2_FUNCTIONS = ['add', 'sub', 'and', 'or', 'xor']
ARITY_1_FUNCTIONS = ['inc', 'dec']

def isint(x):
    try: int(x)
    except: return False
    return True

def deref(scope, arg):
    return arg if isint(arg) else f"QWORD [rsp+{8*(scope['stack'] - scope['args'][arg] - 1)}]"

def make_function_call(scope, fn, args):
    assert len(args) <= len(X86_64_REGISTERS), f"function only support params upto {len(X86_64_REGISTERS)}."

    code = [f"; -- call {fn} with params {' '.join(args)} --"]
    for reg, arg in zip(X86_64_REGISTERS, args):
        code.append(f"mov {reg}, {deref(scope, arg)}")

    code.append(f"{fn} {', '.join(X86_64_REGISTERS[:len(args)])}")
    code.append("push rax")
    scope['args']['_'] = scope['stack']
    scope['stack'] += 1
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
    scope = {'args': {}, 'stack': 0}
    for c in calls:
        # ['assign', str variable name, int literal | str variable ref]
        if c[0] == 'assign':
            arg1, arg2 = c[1], c[2]
            code.append(f"; -- {arg1} = {arg2} --")
            code.append(f"push {deref(scope, arg2)}")

            scope['args']['_'] = scope['args'][arg1] = scope['stack']
            scope['stack'] += 1
        # [<fn>, <int | variable>, <int | variable>]
        elif c[0] in ARITY_2_FUNCTIONS:
            assert len(c) == 3
            code.extend(make_function_call(scope, c[0], c[1:]))
        # [<fn>, <int | variable>]
        elif c[0] in ARITY_1_FUNCTIONS:
            assert len(c) == 2
            code.extend(make_function_call(scope, c[0], c[1:]))
        # ['print', int literal | str variable ref]
        elif c[0] == 'print':
            code.append(f"; -- print {c[1]} to console --")
            code.append(f"mov rdi, {deref(scope, c[1])}")
            code.append(f"call _print")
            # system calls do not have any output
            if '_' in scope['args'] : del scope['args']['_']
        elif c[0] == 'exit':
            code.append(f"; -- exit with code {c[1]} --")
            code.append(f"mov rdi, {deref(scope, c[1])}")
            code.append(f"call _exit")
            # system calls do not have any output
            if '_' in scope['args'] : del scope['args']['_']
        else:
            raise Exception(f'Unknow function call {" ".join(map(str, c))}')
    return '\n'.join(code)