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

from code_generator import generate

if __name__ == '__main__':
    code = generate(
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
            ['add', 5, 10],
            ['print', '_'],
            ['add', 'x', 10],
            ['print', '_'],
            ['add', -5, 'x'],
            ['print', '_'],
            ['add', 'y', 'x'],
            ['print', '_'],
            ['sub', 5, 10],
            ['print', '_'],
            ['sub', 'x', 10],
            ['print', '_'],
            ['sub', -5, 'x'],
            ['print', '_'],
            ['sub', 'y', 'x'],
            ['print', '_'],
            ['and', 10, 2],
            ['print', '_'],
            ['and', 'x', 'y'],
            ['print', '_'],
        ]
    )
    with open('out.asm', 'w+') as f:
        f.write(ASM(code))