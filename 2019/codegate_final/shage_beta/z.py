from json import loads

x = loads(open('data.txt').read())

wtf = {}

for _ in x:
	wtf[_['memo']] = 1
	wtf[_['title']] = 1
	wtf[_['external_url']] = 1
	wtf[_['attachment']] = 1

for k, v in wtf.items():
	print k