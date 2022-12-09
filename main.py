ASM = lambda code: f"""
segment .text
global _start

print:
sub     rsp, 40
mov     eax, edi
mov     esi, 1
mov     r9d, 3435973837
neg     eax
mov     BYTE [rsp+31], 10
lea     r8, [rsp+30]
cmovs   eax, edi
.L2:
mov     edx, eax
mov     r10d, esi
sub     r8, 1
imul    rdx, r9
add     esi, 1
shr     rdx, 35
lea     ecx, [rdx+rdx*4]
add     ecx, ecx
sub     eax, ecx
add     eax, 48
mov     BYTE [r8+1], al
mov     eax, edx
test    edx, edx
jne     .L2
test    edi, edi
jns     .L3
mov     eax, 31
sub     eax, esi
lea     esi, [r10+2]
cdqe
mov     BYTE [rsp+rax], 45
.L3:
movsx   rdx, esi
mov     eax, 32
mov     edi, 1
sub     rax, rdx
mov     edx, esi
add     rax, rsp
mov     rsi, rax
xor     eax, eax
mov     rax, 1
syscall
add     rsp, 40
ret

_start:
{code}
mov rax, 60
mov rdi, 0
syscall
"""

def main(calls):
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
            del scope['_']
    return '\n'.join(code)

if __name__ == '__main__':
    code = main(
        [
            ['assign', 'x', 10],
            ['print', 20],
            ['print', 'x'],
            ['assign', 'y', 30],
            ['print', 'y'],
            ['assign', 'z', 'y'],
            ['print', 'z'],
            ['print', -10],
            ['assign', 'a', -12],
            ['print', 'a'],
        ]
    )
    with open('out.asm', 'w+') as f:
        f.write(ASM(code))