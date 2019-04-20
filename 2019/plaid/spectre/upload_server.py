#!/usr/bin/env python

import sys,  time

from requests import get, post
from pprint import pprint

try:
    my_file = sys.argv[2]
except:
    my_file = None


token = sys.argv[1]

url = 'http://spectre.pwni.ng:4000/'
files = {
    'script': open(my_file if my_file else 'bin.bin', 'rb'),
}

data = {
    'pow': token
}

c = post(url, data=data, files=files)
result = c.history[0].headers['Location']

while True:
    c = get(result)
    data = c.content

    if not '00000000 00000000' in data:
        time.sleep(1)
        continue

    break

if '00000000 00000000' in data:
    # processing 4141 mem
    mem = []
    _ = data.split('<pre style="background-color: white; margin: 2rem 0; padding: 2rem 0">')[1].split('</pre>')[0].strip().replace(' ', '').replace('\n', '')
    for i in xrange(0, len(_), 16):
        low = int(_[i: i+8], 16)
        high = int(_[i+8: i+16], 16) << 32
        q = low + high
        if q == 0: q = 0xffffffff
        mem.append(q)

    print(mem)
    print(min(mem))
    print(mem.index(min(mem)))



else:
    print(data)
