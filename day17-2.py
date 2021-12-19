import numpy as np
from collections import defaultdict

def solve(tx,ty):

    xs = defaultdict( lambda : [10000,-10000])

    ovx = np.arange(200)
    vx = ovx.copy()
    x = np.zeros(200)
    for t in range(2000):
        x += vx
        vx = np.maximum(vx-1, 0)
        #print(ovx[(x>=tx[0]) & (x<=tx[1])])
        for v in ovx[(x>=tx[0]) & (x<=tx[1])]:
            xs[v][0] = min(xs[v][0], t)
            xs[v][1] = max(xs[v][1], t)

    print(xs)

    ys = defaultdict(lambda : [0,None,10000,-10000])

    for vy in range(-1000,1000):
        y = 0
        v = vy
        m = 0
        for t in range(0,2000):
            y += v
            v -= 1
            m = max(m,y)
            if y>=ty[0] and y<=ty[1]:
                ys[vy][0] = max(ys[vy][0],m)
                ys[vy][1] = y
                ys[vy][2] = min(ys[vy][2], t)
                ys[vy][3] = max(ys[vy][3], t)

    print(ys)

    print('highest', max(ys.values()))

    combos = []
    for xv,x in xs.items():
        for yv,y in ys.items():
            if not (y[2]>x[1] or y[3]<x[0]):
                combos.append((xv,yv))

    #print(combos)
    print(len(combos))


solve([20, 30], [-10,-5])
print('-'*10)
solve([70, 125], [-159,-121])
