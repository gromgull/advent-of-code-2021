import itertools
from collections import defaultdict
import numpy as np

lines = [ l.strip() for l in open('input19.txt') ]

scanners = []
for l in lines:
    if l[:3] == '---': scanners.append([])
    elif l:
        scanners[-1].append([int(x) for x in l.split(',')])

scanners = [ np.array(s) for s in scanners ]

def transform(xyz, signs):

    def t(rows):
        return rows[:,xyz]*signs

    t.params = (xyz, signs)
    return t

# this produces 48 transformations, not 24
transforms = [ transform(xyz, signs) for xyz in itertools.permutations(range(3)) for signs in itertools.product([-1,1],[-1,1],[-1,1]) ]

def align(a,b):
    res = {}
    aset = set(tuple(x) for x in a)
    for t in transforms:
        tb = t(b)
        for x in tb:
            for y in a:
                offset = x-y
                ob = tb-offset

                oset = set(tuple(x) for x in ob)
                c = len(aset.intersection(oset))
                if c>11:
                    res[t,tuple(offset)] = c

    return res

a = np.array([[1, 0, 0],
              [0, 2, 0],
              [0, 0, 3]])

for i, t in enumerate(transforms):
    print(i, t.params)
    print(t(a))

a = np.array([[1,2,3]])
s = set(tuple(t(a)[0]) for t in transforms)

print('transforms', len(s))

alignments = defaultdict(dict)
for i,s1 in enumerate(scanners):
    for j,s2 in enumerate(scanners):
        # this does more work than necessary
        # we could skip comparing 1-0, when we already did 0-1
        # but then I would have to work out how to invert transforms
        if i==j: continue
        a = align(s1,s2)
        if a:
            a = list(a)[0]
            alignments[i][j] = a
            print(i,j,a[0].params, a[1])

scanner = 0
done = set([0])

def walk(scanner):
    res = scanners[scanner]

    for a in alignments[scanner]:
        if a in done:
            print('skipping', scanner, '->', a)
            continue
        print('adding', scanner, '->', a)
        transform, offset = alignments[scanner][a]
        done.add(a)
        res = np.vstack([res, transform(walk(a))-offset])

    return res

beacons = set(tuple(s) for s in walk(0))

print(len(beacons))

done = set([0])

def walk2(scanner):
    res = np.array([[0,0,0]])

    for a in alignments[scanner]:
        if a in done:
            print('skipping', scanner, '->', a)
            continue
        print('adding', scanner, '->', a)
        transform, offset = alignments[scanner][a]
        done.add(a)
        res = np.vstack([res, transform(walk2(a))-offset])

    return res

ss = walk2(0)

dist = []
for x in ss:
    for y in ss:
        dist.append(np.abs(x-y).sum())

print(sorted(dist))
