def generate(calls):
    code = []
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
        # ['print', int literal | str variable ref]
        elif c[0] == 'print':
            code.append(f"; -- print {c[1]} to console --")
            if type(c[1]) is int:
                code.append(f"mov rdi, {c[1]}")
            else:
                code.append(f"mov rdi, [rsp+{8*(stack - scope[c[1]] - 1)}]")
            code.append(f"call print")
            if '_' in scope : del scope['_']
    return '\n'.join(code)