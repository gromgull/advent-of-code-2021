import numpy as np
from queue import PriorityQueue
from collections import defaultdict

cave = np.array([list(l.strip()) for l in open('input15.txt')], dtype=int)

print(cave)

def shortest(cave):
    start = (0,0)
    end = (cave.shape[0]-1, cave.shape[1]-1)

    best = defaultdict(lambda : 9999999999)
    best[start] = 0

    edge = PriorityQueue()

    edge.put((0,start))

    i = 0
    while True:
        s, p = edge.get()

        if p == end: break

        for x,y in zip([-1,1,0,0], [0,0,-1,1]):
            new = (p[0]+x, p[1]+y)
            if new[0]<0 or new[0]>end[0] or new[1]<0 or new[1]>end[1]: continue

            ns = best[p] + cave[new]
            if ns < best[new]:
                best[new] = ns
                edge.put((ns + abs(end[0]-new[0]) + abs(end[1]-new[1]), new))
        i += 1
        #print(i)
        #if i>20: break

    return best[end]


print(shortest(cave))

ncave = np.tile(cave, (5,5))

t = np.tile(np.repeat(np.arange(5),cave.shape[0]).reshape((1,5*cave.shape[0])), (cave.shape[1]*5,1))
ncave += t
t = np.tile(np.repeat(np.arange(5),cave.shape[1]).reshape((1,5*cave.shape[1])), (cave.shape[0]*5,1)).T
ncave += t

# ugh
i = ncave>9
ncave[i] %= 10
ncave[i] += 1
print(ncave)

print(shortest(ncave))
