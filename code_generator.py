def generate(calls):
    code = [
        'section .text',
        'global _start',
        'extern _print',
        'extern _exit',
        '; -- entrypoint --',
        '_start:',
    ]
    scope = {}
    stack = 0
    for c in calls:
        # ['assign', str variable name, int literal | str variable ref]
        if c[0] == 'assign':
            var, val = c[1], c[2]
            if type(val) is int:
                code.append(f"; -- {var} = {val} --")
                code.append(f"push {val}")
                scope[var] = stack
                stack += 1
            else:
                scope[var] = scope[val]
            scope['_'] = scope[var]
        # ['add', int literal | str variable ref, int literal | str variable ref]
        elif c[0] == 'add':
            arg1, arg2 = c[1], c[2]

            code.append(f"; -- add {arg1} {arg2} --")
            if type(arg1) is int:
                code.append(f"mov rax, {arg1}")
            else:
                code.append(f"mov rax, [rsp+{8*(stack - scope[arg1] - 1)}]")

            if type(arg2) is int:
                code.append(f"mov rbx, {arg2}")
            else:
                code.append(f"mov rbx, [rsp+{8*(stack - scope[arg2] - 1)}]")
            
            code.append("add rax, rbx")
            code.append("push rax")
            scope['_'] = stack
            stack += 1
        # ['sub', int literal | str variable ref, int literal | str variable ref]
        elif c[0] == 'sub':
            arg1, arg2 = c[1], c[2]

            code.append(f"; -- add {arg1} {arg2} --")
            if type(arg1) is int:
                code.append(f"mov rax, {arg1}")
            else:
                code.append(f"mov rax, [rsp+{8*(stack - scope[arg1] - 1)}]")

            if type(arg2) is int:
                code.append(f"mov rbx, {arg2}")
            else:
                code.append(f"mov rbx, [rsp+{8*(stack - scope[arg2] - 1)}]")

            code.append("sub rax, rbx")
            code.append("push rax")
            scope['_'] = stack
            stack += 1
        # ['and', int literal | str variable ref, int literal | str variable ref]
        elif c[0] == 'and':
            arg1, arg2 = c[1], c[2]

            code.append(f"; -- or {arg1} {arg2} --")
            if type(arg1) is int:
                code.append(f"mov rax, {arg1}")
            else:
                code.append(f"mov rax, [rsp+{8*(stack - scope[arg1] - 1)}]")

            if type(arg2) is int:
                code.append(f"mov rbx, {arg2}")
            else:
                code.append(f"mov rbx, [rsp+{8*(stack - scope[arg2] - 1)}]")
            
            code.append("and rax, rbx")
            code.append("push rax")
            scope['_'] = stack
            stack += 1
        # ['or', int literal | str variable ref, int literal | str variable ref]
        elif c[0] == 'or':
            arg1, arg2 = c[1], c[2]

            code.append(f"; -- or {arg1} {arg2} --")
            if type(arg1) is int:
                code.append(f"mov rax, {arg1}")
            else:
                code.append(f"mov rax, [rsp+{8*(stack - scope[arg1] - 1)}]")

            if type(arg2) is int:
                code.append(f"mov rbx, {arg2}")
            else:
                code.append(f"mov rbx, [rsp+{8*(stack - scope[arg2] - 1)}]")

            code.append("or rax, rbx")
            code.append("push rax")
            scope['_'] = stack
            stack += 1
        # ['xor', int literal | str variable ref, int literal | str variable ref]
        elif c[0] == 'xor':
            arg1, arg2 = c[1], c[2]

            code.append(f"; -- xor {arg1} {arg2} --")
            if type(arg1) is int:
                code.append(f"mov rax, {arg1}")
            else:
                code.append(f"mov rax, [rsp+{8*(stack - scope[arg1] - 1)}]")

            if type(arg2) is int:
                code.append(f"mov rbx, {arg2}")
            else:
                code.append(f"mov rbx, [rsp+{8*(stack - scope[arg2] - 1)}]")

            code.append("xor rax, rbx")
            code.append("push rax")
            scope['_'] = stack
            stack += 1
        # ['print', int literal | str variable ref]
        elif c[0] == 'print':
            code.append(f"; -- print {c[1]} to console --")
            if type(c[1]) is int:
                code.append(f"mov rdi, {c[1]}")
            else:
                code.append(f"mov rdi, [rsp+{8*(stack - scope[c[1]] - 1)}]")
            code.append(f"call _print")
            # system calls do not have any output
            if '_' in scope : del scope['_']
        elif c[0] == 'exit':
            code.append(f"; -- exit with code {c[1]} --")
            if type(c[1]) is int:
                code.append(f"mov rdi, {c[1]}")
            else:
                code.append(f"mov rdi, [rsp+{8*(stack - scope[c[1]] - 1)}]")
            code.append(f"call _exit")
            # system calls do not have any output
            if '_' in scope : del scope['_']
        else:
            raise Exception(f'Unknow function call {" ".join(map(str, c))}')
    return '\n'.join(code)