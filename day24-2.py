from tqdm import tqdm
from itertools import product
from functools import cache

prog = [ line.strip().split(' ') for line in open('input24.txt') ]
prog = [ [ line[0] ] + [ int(x) if x not in 'wxyz' else x for x in line[1:]] for line in prog ]

progs = [ prog[i*18:i*18+18] for i in range(14) ]


# x = z % 26
# z /= 1 | 26
# x += 11 | 14 ...
# x = not x == w
# z *= x*25 + 1 # either 1 or 26
# z += (w+8) * x

@cache
def f(w, z, a, b, c):
    x = (z%26) + b
    print(w,x)
    x = 0 if x == w else 1
    z //= a
    z *= x*25 + 1
    z += (w+c)*x
    return z

def base26(x):
    res = []
    while x:
        res.append(x%26)
        x //= 26
    return list(reversed(res))

progs = [ (p[4][2], p[5][2], p[15][2]) for p in progs ]

print(''.join(['%4d'%x[0] for x in progs]))
print(''.join(['%4d'%x[1] for x in progs]))
print(''.join(['%4d'%x[2] for x in progs]))


def evl(inp):
    z = 0
    for i,p in zip(inp, progs):

        z = f(i, z, *p)
        print(i, p, base26(z))
    return z, inp


def model_numbers():
    yield from product(*(range(1,10) for _ in range(14)))


# smallest
# start = [int(x) for x in '51131616112781']

# largest
start = [int(x) for x in '92793949489995']
print(evl(start))
