from functools import reduce
from collections import namedtuple

node = namedtuple('node', ['version', 'type', 'val'])


def decode(s):

    b = ''.join([f'{int(x,16):0>4b}' for x in s])

    return unpack(b)

def unpack(b):

    version = int(b[:3],2)
    type = int(b[3:6], 2)
    b = b[6:]

    res = None
    if type == 4:
        res = ''
        while True:
            res += b[1:5]
            done = b[0] == '0'
            b = b[5:]
            if done: break
        res = int(res, 2)

    else:
        if b[0]=='1':
            l = int(b[1:12], 2)
            b = b[12:]
            res = []
            for i in range(l):
                nod, nb = unpack(b)
                res.append(nod)
                b = nb

        else:
            l = int(b[1:16], 2)
            res = []
            b = b[16:]
            while True:
                nod, nb = unpack(b)
                res.append(nod)
                l -= len(b)-len(nb)
                b = nb
                if not l: break

    return node(version, type, res), b

def traverse(n, f):
    f(n)
    if isinstance(n.val, list):
        for x in n.val: traverse(x, f)

def eval(l):

    if l.type == 4: return l.val

    val = [ eval(n) for n in l.val ]

    match l.type:
        case 0:
            return sum(val)
        case 1:
            return reduce(lambda a,b: a*b, val)
        case 2:
            return min(val)
        case 3:
            return max(val)
        case 5:
            return 1 if val[0]>val[1] else 0
        case 6:
            return 1 if val[0]<val[1] else 0
        case 7:
            return 1 if val[0] == val[1] else 0


#print(decode('D2FE28'))
#print(decode('38006F45291200'))
#print(decode('EE00D40C823060'))
#print(decode('A0016C880162017C3686B18A3D4780'))

#inp = 'A0016C880162017C3686B18A3D4780'
#inp = 'C200B40A82'
inp = next(open('input16.txt')).strip()

a = decode(inp)[0]
print(a)
counts = []
traverse(a, lambda x: counts.append(x.version))
print(sum(counts))
print(eval(a))
