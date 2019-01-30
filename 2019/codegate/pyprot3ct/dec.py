#!/usr/bin/python
res = 15164928151071436234

for i in range(127):
    res = ((res << 7) & 2**64-1) | res >> 0x39
    res = (res >> 0x20) | ((res & (2**32-1)) << 32)
    n1 = res & 2**32-1
    n2 = res >> 0x20
    n1 = ((n1 - 0xffc2bdec) & 2**32-1) ^ 0xffc2bdec
    n2 = ((n2 - 0xffc2bdec) & 2**32-1) ^ 0xffc2bdec
    res = n1 << 32 | n2

X = hex(res)[2:-1]
print X[8:].decode('hex') + X[0:8].decode('hex')
