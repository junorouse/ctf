from pwn import *
import re
from pprint import pprint

ansi_escape = re.compile(r'\x1B\[([0-?]*[ -/]*[@-~])')


r = remote('110.10.147.125', 20489)
# r = remote('172.17.0.2', 20489)
r.sendline('')
r.sendline('')

name = '@@@@'
r.sendline(name)

r.sendline('')

def get_map(wtfwtf=False):
    MAP = range(22)

    r.recvuntil('o----------------------------------------------------------o')

    data = r.recvuntil('o----------------------------------------------------------o').replace('\x1b[47m#', 'J').split('\n')

    index = 0
    for x in data[1:-1]:
        # re.compile(r'\x1b\[\d{1,2}+X').sub('', x)
        # _ = repr(re.compile(r'\x1b\[\d+X').findall('juno${0}', x))
        for _ in re.findall(r'\x1b\[\d+X', x):
            x = x.replace(_, ' ' * int(_.split('\x1b[')[1].split('X')[0]))
        
        MAP[index] = bytearray(ansi_escape.sub('', x).split('|\x1b(B')[0][1:])
        index += 1

    if wtfwtf == True:
        pprint(data)

    return MAP

def bfs(grid, start, goal, go=0):
    # go = 1 -> next
    # go = -1 -> prev
    queue = collections.deque([[start]])
    seen = set([start])

    if go != 0:
        ban = bytearray('><:msabcdezxv ')
    else:
        ban = bytearray(':msabcdezxv ')

    while queue:
        path = queue.popleft()
        x, y = path[-1]
        
        if grid[y][x] == goal:
            return path

        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < 58 and 0 <= y2 < 22 and grid[y2][x2] in ban and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))


    print 'done'

def make_path(_):
    if _ is None:
        return None
`
    p1 = _[0][0]
    p2 = _[0][1]

    s = ''

    print _

    for i in xrange(1, len(_)):
        if _[i][0] + 1 == p1:
            s += 'h'
        elif _[i][0] - 1 == p1:
            s += 'k'
        elif _[i][1] + 1 == p2:
            s += 'u'
        elif _[i][1] - 1 == p2:
            s += 'j'
        else:
            print 'wtf?'

        p1 = _[i][0]
        p2 = _[i][1]


    # s += 'g'
    
    print 'path!', s
    return s




def find_path(_map, what, go=0):
    table = ":msabcdezxv "

    # get my path
    for i in xrange(len(_map)):
        my_rc = _map[i].find('J')
        if my_rc != -1:
            break

    # print i, my_rc

    if what in '<>':
        go = 1

    return make_path(bfs(_map, (my_rc, i), ord(what), go))


get_map()

def action(what):
    _ = get_map()

    path = find_path(_, what)

    if path is None:
        return None

    len_path = len(path)
    if what in 'abcde':
        path = path+'g'
    elif what in '<>':
        len_path
    elif what == 'm':
        path += 'm'

    
    r.sendline(path)

    for i in xrange(len_path):
        get_map()

    return True


# count = 0

# while True:
#     if action('e') is None:
#         print 'none..'
#         _ = get_map()
#         action('>')
#         r.sendline('h')
#     else:
#         count += 1

#     if count == 10:
#         break
    
action('e')
action('>')
action('<')

for i in xrange(5):
    action('e')
    action('>')
    action('<')
    r.sendline('h')
    get_map()
    get_map()

action('>')
action('>')

#################
action('m')
r.sendline('0')
r.sendline('1')
r.sendline('m')
r.sendline('2')
r.sendline('3')
r.sendline('m')
r.sendline('4')
r.sendline('5')
r.sendline('m')
r.sendline('0')
r.sendline('2')

for i in xrange(11):
    print 'done', i
    get_map()

################# second phase

for i in xrange(4):
    action('e')
    action('>')
    action('<')
    # r.sendline('h')
    get_map()
    # get_map()


#################
action('m')
r.sendline('1')
r.sendline('2')
r.sendline('m')
r.sendline('3')
r.sendline('5')
r.sendline('m')
r.sendline('1')
r.sendline('3')

r.sendline('m') # 128, 128
r.sendline('0')
r.sendline('1')

for i in xrange(8 + 3):
    print 'done', i
    get_map()


######### third phase
for i in xrange(4):
    print 'done', i
    action('e')
    action('>')
    action('<')
    # r.sendline('h')
    get_map()
    # get_map()

#################
action('m')
r.sendline('1')
r.sendline('2')
r.sendline('m')
r.sendline('3')
r.sendline('5')

for i in xrange(5):
    print 'done', i
    get_map()

#################
action('m')
r.sendline('1')
r.sendline('3')

for i in xrange(2):
    print 'done', i
    get_map()



######### fourth phase
for i in xrange(3):
    action('e')
    action('>')
    action('<')
    get_map()

#################
action('m')
r.sendline('2')
r.sendline('3')
r.sendline('m')
r.sendline('2')
r.sendline('4')

r.sendline('m')
r.sendline('1')
r.sendline('2')

r.sendline('m')
r.sendline('0')
r.sendline('1')

for i in xrange(11):
    print 'done', i
    get_map()


######### fifth phase
for i in xrange(4):
    action('e')
    action('>')
    action('<')
    get_map()

#################
action('m')
r.sendline('1')
r.sendline('2')
r.sendline('m')
r.sendline('3')
r.sendline('4')
r.sendline('m')
r.sendline('1')
r.sendline('3')

for i in xrange(8):
    print 'done', i
    get_map()


######### sixth phase
for i in xrange(3):
    action('e')
    action('>')
    action('<')
    get_map()

#################
action('m')
r.sendline('2')
r.sendline('3')
r.sendline('m')
r.sendline('4')
r.sendline('5')
r.sendline('m')
r.sendline('2')
r.sendline('4')
r.sendline('m')
r.sendline('1')
r.sendline('2')

for i in xrange(11):
    print 'done', i
    get_map()


######### seventh phase
for i in xrange(4):
    action('e')
    action('>')
    action('<')
    get_map()

############

action('m')
r.sendline('2')
r.sendline('3')
r.sendline('m')
r.sendline('4')
r.sendline('5')
r.sendline('m')
r.sendline('2')
r.sendline('4')

for i in xrange(8):
    print 'done', i
    get_map()


######### 8th phase
for i in xrange(3):
    action('e')
    action('>')
    action('<')
    get_map()

action('m')
r.sendline('3')
r.sendline('4')

for i in xrange(2):
    print 'done', i
    get_map()
############

######### 8th phase
for i in xrange(1):
    action('e')
    action('>')
    action('<')
    get_map()

action('m')
r.sendline('4')
r.sendline('5')
r.sendline('m')
r.sendline('3')
r.sendline('4')

r.sendline('m')
r.sendline('2')
r.sendline('3')

r.sendline('m')
r.sendline('1')
r.sendline('2')

for i in xrange(4 + 3 + 3):
    print 'done', i
    get_map()

action('>')
action('>')
action('m')
r.sendline('0')
r.sendline('1')

for i in xrange(3):
    print 'done', i
    get_map()

print get_map(wtfwtf=True)

# r.interactive()

# raw_input()

print '----------------- [-] new phase -----------------------'
############ new phase
######### 9th phase
action('<')

for i in xrange(5):
    action('e')
    action('>')
    action('<')
    get_map()


action('m')
r.sendline('1')
r.sendline('2')
r.sendline('m')
r.sendline('3')
r.sendline('4')
r.sendline('m')
r.sendline('1')
r.sendline('3')

for i in xrange(8):
    print 'done', i
    get_map()

############### 10th phase

for i in xrange(4):
    action('e')
    action('>')
    action('<')
    get_map()

action('m')
r.sendline('2')
r.sendline('3')
r.sendline('m')
r.sendline('4')
r.sendline('5')
r.sendline('m')
r.sendline('2')
r.sendline('4')
r.sendline('m')
r.sendline('1')
r.sendline('2')

for i in xrange(11):
    print 'done', i
    get_map()



############### 11st phase

for i in xrange(4):
    action('e')
    action('>')
    action('<')
    get_map()

action('m')
r.sendline('2')
r.sendline('3')
r.sendline('m')
r.sendline('4')
r.sendline('5')
r.sendline('m')
r.sendline('2')
r.sendline('4')
r.sendline('m')
r.sendline('1')
r.sendline('2')

for i in xrange(11):
    print 'done', i
    get_map()


############### 12nd phase

for i in xrange(3):
    action('e')
    action('>')
    action('<')
    get_map()

action('m')
r.sendline('3')
r.sendline('4')

for i in xrange(2):
    print 'done', i
    get_map()


############### 13rd phase

for i in xrange(1):
    action('e')
    action('>')
    action('<')
    get_map()

action('m')
r.sendline('4')
r.sendline('5')

r.sendline('m')
r.sendline('3')
r.sendline('4')

r.sendline('m')
r.sendline('2')
r.sendline('3')

r.sendline('m')
r.sendline('1')
r.sendline('2')

for i in xrange(11):
    print 'done', i
    get_map()



############### 14th phase

for i in xrange(4):
    action('e')
    action('>')
    action('<')
    get_map()

action('m')
r.sendline('2')
r.sendline('3')
r.sendline('m')
r.sendline('4')
r.sendline('5')
r.sendline('m')
r.sendline('2')
r.sendline('4')
r.sendline('m')
r.sendline('1')
r.sendline('2')

for i in xrange(11):
    print 'done', i
    get_map()


############### 15th phase

for i in xrange(3):
    action('e')
    action('>')
    action('<')
    get_map()

action('m')
r.sendline('3')
r.sendline('4')

for i in xrange(2):
    print 'done', i
    get_map()

############


############### 16th phase

for i in xrange(1):
    action('e')
    action('>')
    action('<')
    get_map()

action('m')
r.sendline('4')
r.sendline('5')

r.sendline('m')
r.sendline('3')
r.sendline('4')

r.sendline('m')
r.sendline('2')
r.sendline('3')


for i in xrange(8):
    print 'done', i
    get_map()


############### 17th phase

for i in xrange(3):
    action('e')
    action('>')
    action('<')
    get_map()

action('m')
r.sendline('3')
r.sendline('4')

for i in xrange(2):
    print 'done', i
    get_map()

############### 18th phase

for i in xrange(1):
    action('e')
    action('>')
    action('<')
    get_map()

action('m')
r.sendline('4')
r.sendline('5')

r.sendline('m')
r.sendline('3')
r.sendline('4')

for i in xrange(5):
    print 'done', i
    get_map()


############### 19th phase

for i in xrange(2):
    action('e')
    action('>')
    action('<')
    get_map()

action('m')
r.sendline('4')
r.sendline('5')

for i in xrange(2):
    print 'done', i
    get_map()

action('x')

# r.interactive()

r.sendline('x'*1598)

for i in xrange(1598):
    if i % 100 == 0:
        print 'done', i
    get_map()

action('<')
action('v')
r.sendline('v'*10)

for i in xrange(10):
    if i % 10 == 0:
        print 'done', i
    get_map()


action('>')
get_map()
action('>')
get_map()
action('s')
############### final

# for i in xrange(1):
#     action('a')
#     action('>')
#     action('<')
#     get_map()



# action('e')

# print r.recvall()

# raw_input('?')

r.interactive()

