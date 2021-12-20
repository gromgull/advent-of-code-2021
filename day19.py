from collections import defaultdict
import numpy as np

lines = [ l.strip() for l in open('test19.txt') ]

scanners = []
for l in lines:
    if l[:3] == '---': scanners.append([])
    elif l:
        scanners[-1].append([int(x) for x in l.split(',')])

scanners = [ np.array(s) for s in scanners ]

def transform(front, up):

    rz,ry = [
        [ 0, 0],
        [ 1, 0],
        [ 2, 0],
        [ 3, 0],
        [ 0, 1],
        [ 0, 3]][front]

    crz = np.cos(rz*np.pi/2)
    srz = np.sin(rz*np.pi/2)

    cry = np.cos(ry*np.pi/2)
    sry = np.sin(ry*np.pi/2)

    crx = np.cos(up*np.pi/2)
    srx = np.sin(up*np.pi/2)

    mx = [[1,   0,    0],
          [0, crx, -srx],
          [0, srx,  crx]]
    my = [[cry,  0, sry],
          [0,    1,   0],
          [-sry, 0, cry]]
    mz = [[crz, -srz, 0],
          [srz,  crz, 0],
          [0,      0, 1]]

    m = (np.array(mz, dtype=int) @ my) @ mx

    def t(xyz):
        return np.matmul(xyz, m).astype(int)

    t.params = (front, up)
    return t

transforms = [ transform(front, up) for front in range(6) for up in range(4)]

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
