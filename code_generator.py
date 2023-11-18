def isint(x):
    try:
        int(x)
    except:
        return False
    return True

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
            if isint(arg2):
                code.append(f"; -- {arg1} = {arg2} --")
                code.append(f"push {arg2}")
            else:
                code.append(f"; -- copy {arg2} --")
                code.append(f"push QWORD [rsp+{8*(scope['stack'] - scope['args'][arg2] - 1)}]")

            scope['args']['_'] = scope['args'][arg1] = scope['stack']
            scope['stack'] += 1
        # ['add', int literal | str variable ref, int literal | str variable ref]
        elif c[0] == 'add':
            arg1, arg2 = c[1], c[2]

            code.append(f"; -- add {arg1} {arg2} --")
            if isint(arg1):
                code.append(f"mov rax, {arg1}")
            else:
                code.append(f"mov rax, [rsp+{8*(scope['stack'] - scope['args'][arg1] - 1)}]")

            if isint(arg2):
                code.append(f"mov rbx, {arg2}")
            else:
                code.append(f"mov rbx, [rsp+{8*(scope['stack'] - scope['args'][arg2] - 1)}]")
            
            code.append("add rax, rbx")
            code.append("push rax")
            scope['args']['_'] = scope['stack']
            scope['stack'] += 1
        # ['sub', int literal | str variable ref, int literal | str variable ref]
        elif c[0] == 'sub':
            arg1, arg2 = c[1], c[2]

            code.append(f"; -- add {arg1} {arg2} --")
            if isint(arg1):
                code.append(f"mov rax, {arg1}")
            else:
                code.append(f"mov rax, [rsp+{8*(scope['stack'] - scope['args'][arg1] - 1)}]")

            if isint(arg2):
                code.append(f"mov rbx, {arg2}")
            else:
                code.append(f"mov rbx, [rsp+{8*(scope['stack'] - scope['args'][arg2] - 1)}]")

            code.append("sub rax, rbx")
            code.append("push rax")
            scope['args']['_'] = scope['stack']
            scope['stack'] += 1
        # ['and', int literal | str variable ref, int literal | str variable ref]
        elif c[0] == 'and':
            arg1, arg2 = c[1], c[2]

            code.append(f"; -- or {arg1} {arg2} --")
            if isint(arg1):
                code.append(f"mov rax, {arg1}")
            else:
                code.append(f"mov rax, [rsp+{8*(scope['stack'] - scope['args'][arg1] - 1)}]")

            if isint(arg2):
                code.append(f"mov rbx, {arg2}")
            else:
                code.append(f"mov rbx, [rsp+{8*(scope['stack'] - scope['args'][arg2] - 1)}]")
            
            code.append("and rax, rbx")
            code.append("push rax")
            scope['args']['_'] = scope['stack']
            scope['stack'] += 1
        # ['or', int literal | str variable ref, int literal | str variable ref]
        elif c[0] == 'or':
            arg1, arg2 = c[1], c[2]

            code.append(f"; -- or {arg1} {arg2} --")
            if isint(arg1):
                code.append(f"mov rax, {arg1}")
            else:
                code.append(f"mov rax, [rsp+{8*(scope['stack'] - scope['args'][arg1] - 1)}]")

            if isint(arg2):
                code.append(f"mov rbx, {arg2}")
            else:
                code.append(f"mov rbx, [rsp+{8*(scope['stack'] - scope['args'][arg2] - 1)}]")

            code.append("or rax, rbx")
            code.append("push rax")
            scope['args']['_'] = scope['stack']
            scope['stack'] += 1
        # ['xor', int literal | str variable ref, int literal | str variable ref]
        elif c[0] == 'xor':
            arg1, arg2 = c[1], c[2]

            code.append(f"; -- xor {arg1} {arg2} --")
            if isint(arg1):
                code.append(f"mov rax, {arg1}")
            else:
                code.append(f"mov rax, [rsp+{8*(scope['stack'] - scope['args'][arg1] - 1)}]")

            if isint(arg2):
                code.append(f"mov rbx, {arg2}")
            else:
                code.append(f"mov rbx, [rsp+{8*(scope['stack'] - scope['args'][arg2] - 1)}]")

            code.append("xor rax, rbx")
            code.append("push rax")
            scope['args']['_'] = scope['stack']
            scope['stack'] += 1
        # ['print', int literal | str variable ref]
        elif c[0] == 'print':
            code.append(f"; -- print {c[1]} to console --")
            if isint(c[1]):
                code.append(f"mov rdi, {c[1]}")
            else:
                code.append(f"mov rdi, [rsp+{8*(scope['stack'] - scope['args'][c[1]] - 1)}]")
            code.append(f"call _print")
            # system calls do not have any output
            if '_' in scope['args'] : del scope['args']['_']
        elif c[0] == 'exit':
            code.append(f"; -- exit with code {c[1]} --")
            if isint(c[1]):
                code.append(f"mov rdi, {c[1]}")
            else:
                code.append(f"mov rdi, [rsp+{8*(scope['stack'] - scope['args'][c[1]] - 1)}]")
            code.append(f"call _exit")
            # system calls do not have any output
            if '_' in scope['args'] : del scope['args']['_']
        else:
            raise Exception(f'Unknow function call {" ".join(map(str, c))}')
    return '\n'.join(code)