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
transforms = [ transform(xyz, signs) for xyz in itertools.permutations(range(3)) for signs in itertools.product([1,-1],[1,-1],[1,-1]) ]

def align(a,b):

    x = constellations[a][0]

    ts = []
    for t in constellations[b]:
        c = len(x.intersection(constellations[b][t]))
        if c>3:
            ts.append(transforms[t])
            #print(a,b,transforms[t].params,c)

    aset = set(tuple(x) for x in scanners[a])
    for t in ts:
        tb = t(scanners[b])
        for x in tb:
            for y in scanners[a]:
                offset = x-y
                ob = tb-offset

                oset = set(tuple(x) for x in ob)
                c = len(aset.intersection(oset))
                if c>11:
                    return t,tuple(offset)


a = np.array([[1, 0, 0],
              [0, 2, 0],
              [0, 0, 3]])

for i, t in enumerate(transforms):
    print(i, t.params)
    print(t(a))

a = np.array([[1,2,3]])
s = set(tuple(t(a)[0]) for t in transforms)

print('transforms', len(s))

constellations = defaultdict(lambda : defaultdict(set))
for i,s in enumerate(scanners):

    for a in s:
        c = a-s
        for j,t in enumerate(transforms):
            constellations[i][j].update(tuple(o) for o in t(c))

alignments = defaultdict(dict)
for i,s1 in enumerate(scanners):
    for j,s2 in enumerate(scanners):
        # this does more work than necessary
        # we could skip comparing 1-0, when we already did 0-1
        # but then I would have to work out how to invert transforms
        if i==j: continue
        a = align(i,j)
        if a:
            alignments[i][j] = a
            print(i,j,a[0].params, a[1])

scanner = 0
done = set([0])

def walk(scanner, key):
    res = key(scanner)

    for a in alignments[scanner]:
        if a in done:
            print('skipping', scanner, '->', a)
            continue
        print('adding', scanner, '->', a)
        transform, offset = alignments[scanner][a]
        done.add(a)
        res = np.vstack([res, transform(walk(a, key))-offset])

    return res

beacons = set(tuple(s) for s in walk(0, lambda s: scanners[s]))

print(len(beacons))

done = set([0])

ss = walk(0, key=lambda _: np.array([[0,0,0]]))

dist = []
for x in ss:
    for y in ss:
        dist.append(np.abs(x-y).sum())

print(max(dist))
