import numpy as np
import re
from itertools import product

def flatten(t):
    return [item for sublist in t for item in sublist]

class MyTotallyRealSparse3dArray():

    def __init__(self, size):
        self.size = size
        self.slices = []

    def _split_d(self, s, split):
        if split>s.start and split<s.stop:
            return [ slice(s.start, split), slice(split, s.stop) ]
        return [ s ]

    def _split_cube(self, slices, splits):
        rs = []
        for s,sp in zip(slices, splits):
            rs.append(self._split_d(s,sp))
        return list(product(*rs))


    def _find_splits_d(self, a, b):
        res = []
        if b.start>=a.start and b.start<a.stop:
            res.append(b.start)
        if b.stop>a.start and b.stop<=a.stop:
            res.append(b.stop)
        if a.start>=b.start and a.start<b.stop:
            res.append(a.start)
        if a.stop>b.start and a.stop<=b.stop:
            res.append(a.stop)

        return res

    def _find_splits(self, a, b):
        return list(product(*[ self._find_splits_d(x,y) for x,y in zip(a,b) ]))

    def __setitem__(self, idx, val):

        import ipdb ; ipdb.set_trace()

        splits = []
        for s in self.slices:
            splits += self._find_splits(s, idx)

        idx = [idx]
        for split in splits:
            idx = flatten([ self._split_cube(i, split) for i in idx ])

        if val:
            for i in idx:
                if not any(self._find_splits(i, s) for s in self.slices): self.slices.append(i)




    def nonzero(self):
        return np.sum([ np.prod( [ d[1]-d[0] for d in s ] ) for s in self.slices ] )


lines = [ l.strip().split(' ') for l in open('test22-1.txt') ]
lines = [ (l[0] == 'on', [ c.split('..') for c in re.sub('.=', '', l[1]).split(',') ]) for l in lines ]
lines = [ (l[0], [ (int(c[0]), int(c[1])+1) for c in l[1] ]) for l in lines ]

max_ = np.max([[c[1] for c in l[1]] for l in lines], axis=0)
min_ = np.min([[c[0] for c in l[1]] for l in lines], axis=0)

print(lines)

init = False

if init:
    size = [101,101,101]
else:

    size = max_-min_


data = MyTotallyRealSparse3dArray(size)

def bnds(i):
    return max(i,0)

def bounds(c):

    return [ slice(bnds(x[0]-mi), bnds(x[1]-mi)) for x,mi in zip(c, min_) ]

for val, cube in lines:
    print(bounds(cube))
    data[bounds(cube)] = val

print(data.nonzero())
