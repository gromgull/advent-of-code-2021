import numpy as np
lines = [ l.strip() for l in open('input20.txt') ]

code = [ 0 if c=='.' else 1 for c in lines[0] ]
floor = np.array([ [ 0 if c=='.' else 1 for c in l ] for l in lines[2:] ])

k = np.ogrid[-1:2,-1:2]
bin = 2**np.arange(9,dtype=int)[::-1]

def process(a, i):

    inp = np.zeros((a.shape[0]+8, a.shape[1]+8), dtype=int)
    res = inp.copy()

    if code[0] and not i%2: res.fill(1)
    if code[0] and i%2: inp.fill(1)

    inp[4:-4,4:-4] = a

    for x in range(-2, a.shape[0]+2):
        for y in range(-2, a.shape[1]+2):
            res[4+x,4+y] = code[(inp[(4+k[0]+x, 4+k[1]+y)].flat * bin).sum()]

    return res

r = floor
for i in range(50):
    print(i)
    # for l in r:
    #     print(''.join([ '#' if c else '.' for c in l ]))

    r = process(r, i)

# for l in r:
#     print(''.join([ '#' if c else '.' for c in l ]))


print(r.nonzero()[0].size)
