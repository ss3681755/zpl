X86_64_REGISTERS = ['rax', 'rdi', 'rsi', 'rdx', 'r10', 'r8', 'r9']
ARITY_2_FUNCTIONS = ['add', 'sub', 'and', 'or', 'xor']
ARITY_1_FUNCTIONS = ['inc', 'dec']

def isint(x):
    try: int(x)
    except: return False
    return True

def to_arg(args):
    return [a['value'] for a in args]

def deref(scope, arg):
    return arg if isint(arg) else f"QWORD [rsp+{8*(scope['stack'] - scope['args'][arg] - 1)}]"

def make_name_call(scope, fn, args):
    assert len(args) <= len(X86_64_REGISTERS), f"name only support params upto {len(X86_64_REGISTERS)}."

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
    index = 0
    while index < len(calls):
        c = calls[index]
        # ['assign', str variable name, int literal | str variable ref]
        if c['name'] == 'assign':
            arg1, arg2 = to_arg(c['arguments'])
            code.append(f"; -- {arg1} = {arg2} --")
            code.append(f"push {deref(scope, arg2)}")

            scope['args']['_'] = scope['args'][arg1] = scope['stack']
            scope['stack'] += 1
        # [<fn>, <int | variable>, <int | variable>]
        elif c['name'] in ARITY_2_FUNCTIONS:
            assert len(c['arguments']) == 2
            code.extend(make_name_call(scope, c['name'], to_arg(c['arguments'])))
        # [<fn>, <int | variable>]
        elif c['name'] in ARITY_1_FUNCTIONS:
            assert len(c['arguments']) == 1
            code.extend(make_name_call(scope, c['name'], to_arg(c['arguments'])))
        elif c['name'] == 'div':
            arg1, arg2 = to_arg(c['arguments'])
            # find a way to handle divide by 0 error before generating the asm
            code.append(f"; -- call {c['name']} with params {' '.join(to_arg(c['arguments']))} --")
            code.append("xor rdx, rdx")
            code.append(f"mov rax, {deref(scope, arg1)}")
            code.append(f"mov rdi, {deref(scope, arg2)}")
            code.append(f"div rdi")
            code.append("push rax")
            scope['args']['_'] = scope['stack']
            scope['stack'] += 1
        elif c['name'] == 'rem':
            arg1, arg2 = to_arg(c['arguments'])
            # find a way to handle divide by 0 error before generating the asm
            code.append(f"; -- call {c['name']} with params {' '.join(to_arg(c['arguments']))} --")
            code.append("xor rdx, rdx")
            code.append(f"mov rax, {deref(scope, arg1)}")
            code.append(f"mov rdi, {deref(scope, arg2)}")
            code.append(f"div rdi")
            code.append("push rdx")
            scope['args']['_'] = scope['stack']
            scope['stack'] += 1
        elif c['name'] == 'mul':
            arg1, arg2 = to_arg(c['arguments'])
            code.append(f"; -- call {c['name']} with params {' '.join(to_arg(c['arguments']))} --")
            code.append(f"mov rax, {deref(scope, arg1)}")
            code.append(f"mov rdi, {deref(scope, arg2)}")
            code.append(f"mul rdi")
            code.append("push rax")
            scope['args']['_'] = scope['stack']
            scope['stack'] += 1
        # ['print', int literal | str variable ref]
        elif c['name'] == 'print':
            assert len(c['arguments']) == 1
            arg1 = to_arg(c['arguments'])[0]
            code.append(f"; -- print {arg1} to console --")
            code.append(f"mov rdi, {deref(scope, arg1)}")
            code.append(f"call _print")
            # system calls do not have any output
            if '_' in scope['args'] : del scope['args']['_']
        elif c['name'] == 'exit':
            assert len(c['arguments']) == 1
            arg1 = to_arg(c['arguments'])[0]
            code.append(f"; -- exit with code {arg1} --")
            code.append(f"mov rdi, {deref(scope, arg1)}")
            code.append(f"call _exit")
            # system calls do not have any output
            if '_' in scope['args'] : del scope['args']['_']
        else:
            raise Exception(f'Unknow name call {" ".join(map(str, c))}')
        index += 1
    return '\n'.join(code)