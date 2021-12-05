from collections import Counter

lines = [ [ [ int(c) for c in x.split(',')]
           for x in l.strip().split(' -> ')] for l in open('input5.txt') ]

def rnge(a,b):
    s = 1 if a<b else -1
    return range(a,b+s,s)

def line(a, b, straight=False):
    x1,y1 = a
    x2,y2 = b

    if x1 == x2:
        return [ (x1,y) for y in rnge(y1,y2) ]
    elif y1 == y2:
        return [ (x,y1) for x in rnge(x1,x2) ]
    elif straight:
        return [ (x,y) for x,y in zip(rnge(x1,x2), rnge(y1,y2)) ]
    else:
        return []

c = Counter()

for l in lines:
    c.update(line(*l))


print(len([ k for k in c if c[k]>=2 ]))

c = Counter()

for l in lines:
    c.update(line(*l, True))

print(len([ k for k in c if c[k]>=2 ]))
