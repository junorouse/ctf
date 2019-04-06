from requests import get, put

cookie = 'session=4b362d57-2ea8-4f1e-93cb-90fac2e238f4'
url = 'http://110.10.147.124/stars?page={}'

headers = {
    'Cookie': cookie,
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-CSRF-Token': 'IjhmN2MzZGQ0MGY0ZTEzNzQ2MmQ1NGE3YThhYmNmYTAyYmIxYmM2YzYi.XJqScg.KYvCK9MrXqSlguAekdfjDymZW94'

}

share_url_list = []

for i in xrange(1, 16+1):
    c = get(url.format(i),  headers = headers).content
    x = c.split('<input class="calendar-share-url"')[1:]
    for k in x:
        share_url_list.append(k.split('value="')[1].split('"')[0])

print share_url_list

url = 'http://110.10.147.124/calendars/import'

for xx in share_url_list:
    data = {
        'url': xx,
    }

    c = put(url, headers=headers, data=data)
    print c.text
    print c.status_code