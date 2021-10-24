import sys
import glob
import select

header = '\x5b\x29\x3e\x1e\x30\x36'


class Scanner(object):
    def __init__(self):
        self.scanner = None
        self.field_map = {}
        self.current_po = None
        self.total = 0
        self.find_scanner()

    def find_scanner(self):
        s = glob.glob('/dev/serial/by-id/*Symbol_Bar_Code_Scanner*')
        if len(s) == 1:
            self.scanner = open(s[0], 'r')
            print('Found Symbol scanner')
        else:
            print('No Scanner found')
            sys.exit(0)

    def drain(self):
        n = 0
        inputs = [self.scanner, ]
        while 1:
            i, o, e = select.select(inputs, [], [], 0)
            if len(i) > 0:
                i[0].read(1)
                n += 1
                # print('Reading from ', f)
            else:
                break
        return n

    def read(self):
        inputs = [self.scanner, ]
        i, o, e = select.select(inputs, [], [])
        if len(i) > 0:
            r = i[0].readline()
        else:
            r = None
        return r

    @staticmethod
    def decode_ecia(bc):
        global header
        d = {}
        fields = bc.split('\x1d')

        # print(fields)
        for f in fields:
            f = f.strip('\x1e\n')
            if f == header:
                d['type'] = 'ecia'
            if f.startswith('P'):
                d['P'] = f[1:].split(' ')[0]
            if f.startswith('1P'):
                d['1P'] = f[2:]
            if f.startswith('9D'):
                d['9D'] = f[2:]
            if f.startswith('10D'):
                d['10D'] = f[3:]
            if f.startswith('1T'):
                d['1T'] = f[2:]
            if f.startswith('K'):
                d['K'] = f[1:]
            if f.startswith('1K'):
                d['1K'] = f[2:]
            if f.startswith('10K'):
                d['10K'] = f[3:]
            if f.startswith('11K'):
                d['11K'] = f[3:]
            if f.startswith('4L'):
                d['4L'] = f[2:]
            if f.startswith('Q'):
                d['Q'] = int(f[1:])
            if f.startswith('11Z'):
                d['11Z'] = f[3:]
            if f.startswith('12Z'):
                d['12Z'] = f[3:]
            if f.startswith('13Z'):
                d['13Z'] = f[3:]
            if f.startswith('20Z'):
                d['20Z'] = f[3:]
            if f.startswith('10R'):
                d['10R'] = f[3:]
            if f.startswith('S'):
                d['S'] = f[1:]

        d['bc'] = bc

        return d

    def scan(self):
        global header
        d = {}
        bc = self.read()

        if bc.startswith(header):
            d = self.decode_ecia(bc)
        else:
            fields = bc.strip().split(' ')
            if len(fields) == 1 and len(fields[0]) > 0:
                d['type'] = 'generic'
                d['G'] = fields[0]

            if len(fields) == 2 and fields[0].startswith('3N1'):
                d['type'] = 'panasonic'
                d['1P'] = fields[0][3:]
                d['Q'] = fields[1]

        return d

    def scan_storage(self):
        bc = self.read()

        try:
            bc = bc.strip()  # remove newline
            label = bc.split(':')
            if len(label) != 3 or label[0] != 'DT' or label[1] != 'L':
                return None
            location_id = int(label[2])
            if location_id > 9999 or location_id < 0:
                return None
            return location_id
        except ValueError:
            return None
