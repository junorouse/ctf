from pprint import pprint

f = open("code", "rb")
code = f.read()
code = bytearray(code)
f.close()

_ = {
    'OP': 0,
    'ARGC': 0,
    'ARGS': []
}
pc = 0

OUT = []

try:
    while True:
        _ = {
            'OP': 0,
            'ARGC': 0,
            'ARGS': []
        }

        OP = code[pc]
        pc += 1

        _['OP'] = OP

        ARGC = code[pc]
        pc += 1

        _['ARGC'] = ARGC

        # print OP, ARGC,

        for i in xrange(ARGC):
            _len = code[pc]
            pc += 1
            what = code[pc:pc+_len]
            pc += _len
            _['ARGS'].append(str(what))

        OUT.append(_)
except:
    pass

# print OUT

FMT = 'N{}'
BOX = {}

COUNT = 0

for i in xrange(len(OUT)):
    for k in xrange(len(OUT[i]['ARGS'])):
        if OUT[i]['ARGS'][k].count('0') > 2 and OUT[i]['ARGS'][k].count('O') > 2 and OUT[i]['ARGS'][k].isdigit() == False:
            if OUT[i]['ARGS'][k] in BOX:
                pass
            else:
                BOX[OUT[i]['ARGS'][k]] = FMT.format(COUNT)
                COUNT += 1

            OUT[i]['ARGS'][k] = BOX[OUT[i]['ARGS'][k]]

pprint(OUT)