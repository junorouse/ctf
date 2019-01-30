from pwn import *
import sys

context.arch = 'amd64'
context.terminal = ['tmux', 'splitw', '-h']
KT = [
'',
'lOv3\x00',
'D0l1',
'HuNgRYT1m3',
'F0uRS3aS0n',
'T1kT4kT0Kk',
]

i0 = i1 = i2 = i3 = i4 = i5 = i6 = i7 = i8 = i9 = i10 = 0


'''
for i0 in xrange(1, 3):
    for i1 in xrange(3):
        open('count', 'wb').write(str(i0) + ',' + str(i1))
        for i2 in xrange(3):
            for i3 in xrange(2):
                for i4 in xrange(2):
                    for i5 in xrange(9):
                        for i7 in xrange(2):
                            for i8 in xrange(3):
                                for i9 in xrange(3):
                                    for i10 in xrange(2):

'''

i0 = 1
i1 = 2
i2 = 1
i3 = 0
i4 = 1
i5 = 5
i6 = 0
i7 = 0
i8 = 0
i9 = 2
i10 = 0

# r = process('./d')
r = remote('110.10.147.104', 13152)

r.sendline('1')
r.sendline(KT[1])
r.sendline('1')
r.sendline('2')

def x1(q):
    if q == 0: r.sendline('1')
    elif q == 1: r.sendline('2')
    elif q == 2: r.sendline('3')

def x2(q):
    if q == 0: r.sendline('1')
    elif q == 1: r.sendline('2')
    elif q == 2: r.sendline('3')

def x3(q): # PASS_1
    if q == 0:
        r.sendline('1')
    elif q == 1:
        r.sendline('2')
        r.sendline('1')
        x4(i3)
    elif q == 2:
        r.sendline('3')
        r.sendline('1')

def x4(q):
    if q == 0:
        r.sendline('1')
    elif q == 1:
        r.sendline('2')


def x5(q):
    if q == 0:
        r.sendline('1')
        r.sendline('2')
        r.sendline('2')
    elif q == 1:
        r.sendline('2')
        if i10 == 0:
            r.sendline('1')
        elif i10 == 1:
            r.sendline('2')

def x6(q):
    if q == 0:
        r.sendline('1')
        r.sendline('1')
        r.sendline('2')
    elif q == 1:
        r.sendline('1')
        r.sendline('2')
        r.sendline('1')
    elif q == 2:
        r.sendline('1')
        r.sendline('2')
        r.sendline('3')

    elif q == 3:
        r.sendline('2')
        r.sendline('1')
        r.sendline('2')
    elif q == 4:
        r.sendline('2')
        r.sendline('2')
        r.sendline('1')
    elif q == 5:
        r.sendline('2')
        r.sendline('2')
        r.sendline('3')

    elif q == 6:
        r.sendline('3')
        r.sendline('1')
        r.sendline('2')
    elif q == 7:
        r.sendline('3')
        r.sendline('2')
        r.sendline('1')
    elif q == 8:
        r.sendline('3')
        r.sendline('2')
        r.sendline('3')

def x7(q):
    if q == 0:
        r.sendline('1')
        r.sendline('2')
    elif q == 1:
        r.sendline('2')
        if i7 == 0:
            r.sendline('1')
        elif i7 == 1:
            r.sendline('2')

def x8(q):
    if q == 0:
        r.sendline('1')
        r.sendline('2')
    elif q == 1:
        r.sendline('2')
    elif q == 2:
        r.sendline('1')
        r.sendline('1')
        r.sendline('2')


def x9(q):
    if q == 0:
        r.sendline('2')
        r.sendline('1')
        r.sendline('1')
    elif q == 1:
        r.sendline('2')
        r.sendline('1')
        r.sendline('2')
    elif q == 2:
        r.sendline('3')
        r.sendline('2')

x1(i0)
x2(i1)

r.sendline(KT[2])
r.sendline('1')

x3(i2)
x5(i4)

# r.sendline('1')
# r.sendline('1')
# r.sendline('2')
# r.sendline('2')


r.sendline(KT[3])

x6(i5)

r.sendline(KT[4])

r.sendline('1')
r.sendline('1')
r.sendline('\x00') # BUG

x8(i8)

r.sendline(KT[5])

x9(i9)

# context.log_level = 'debug'
r.recvuntil('King : Congratuations for pass all the tests.')
r.recvuntil('SYSTEM : Your point\n')
data = r.recvuntil('King : Wh').split('\n')
print data

w = []
for i in xrange(5):
    w.append(int(data[i][-1]))

print w

juno = True
for asdf in xrange(5):
    if w[asdf] != 5:
        juno = False
        break


print i0 ,i1 , i2 , i3 , i4 , i5 , i6 , i7 , i8 , i9, i10

if juno:
    print 'FOUND!!!!!!!!!!!!!!'
    r.interactive()

r.close()

                                            

