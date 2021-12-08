from collections import Counter, defaultdict

digits = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg',
}

lookup = { ''.join(sorted(v)):k for k,v in digits.items() }

segments = set('abcdefg')

lenidx = defaultdict(list)
for d,s in digits.items():
    lenidx[len(s)].append(d)

invlenidx = { k: set(range(10)).difference(v) for k,v in lenidx.items() }

invdigits = { d: segments.difference(s) for d,s in digits.items() }

def not_in_any(l):
    r = set()
    r.update(*l)
    return segments.difference(r)

idx2 = { d: not_in_any([ digits[x] for x in lenidx[len(digits[d])]]) for d in digits }

lines = [ [ c.split() for c in x.strip().split('|') ] for x in open('input8.txt') ]

c = Counter()
for l in lines:
    c.update( [ len(x) for x in l[1] ] )

# 1, 4, 7, 8
print(c[2], c[4], c[3], c[7], c[2]+c[4]+c[3]+c[7])

def pm():
    print('----')
    for x in sorted(mappings):
        print(x, ':', "".join(sorted(mappings[x])))


res = 0
for l in lines:

    ten = [set(d) for d in l[0]]

    dm = { d: set(range(10)) for d in range(10) }

    mappings = { s: set(segments) for s in segments }

    pm()
    for i,d in enumerate(l[0]):
        dm[i].difference_update(invlenidx[len(d)])

    invdm = defaultdict(list)
    for i,ds in dm.items():
        for d in ds: invdm[d].append(i)

    # a is in 7, not in 1
    mappings = { k:v.difference(['a']) for k,v in mappings.items() }
    mappings[ten[invdm[7][0]].difference(ten[invdm[1][0]]).pop()] = set('a')
    pm()

    # e is in 2,3,5 not in 4, b in 4
    c = Counter()
    for d in invdm[2]: c.update(ten[d])
    be = { s for s,count in c.items() if count==1 }
    mappings = { k:v.difference(['e', 'b']) for k,v in mappings.items() }
    mappings[be.difference(ten[invdm[4][0]]).pop()] = set('e')
    mappings[be.intersection(ten[invdm[4][0]]).pop()] = set('b')

    pm()

    # e is twice in 0,6,9, but not in 1
    c = Counter()
    for d in invdm[0]: c.update(ten[d])
    edc = { s for s,count in c.items() if count==2 }
    mappings = { k:v.difference(['c','f','d']) for k,v in mappings.items() }
    mappings[edc.intersection(ten[invdm[1][0]]).pop()] = set('c')
    mappings[ten[invdm[1][0]].difference(edc).pop()] = set('f')
    mappings[edc.intersection(ten[invdm[4][0]]).difference(ten[invdm[1][0]]).pop()] = set('d')

    pm()

    v = ''.join([ str(lookup[''.join(sorted(list(mappings[s])[0] for s in v))]) for v in l[1]])
    print(v)

    res += int(v)

print(res)
