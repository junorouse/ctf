from requests import get, post
import time
import json

while True:
    c  = get('http://telooogram.oooverflow.io//msg?token=99aa4446a37deffbc33bdf07d5449067')
    try:
        data = json.loads(c.text)
        for x in data:
            if 'MDAwR'.encode('hex') in x['blob']:
                flag = ('MDAw' + x['blob'].decode('hex').split('MDAw')[1][:60]).decode('base64')
                c = post('http://54.177.169.8:4000/api/submit_flag/'+ flag)
                print c.text
            elif 'eyAidXNlcm'.encode('hex') in x['blob']:
                print 'findfind!!!', x['blob']
    except Exception as e:
        print e
        print 'error'
