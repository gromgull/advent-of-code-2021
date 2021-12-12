from collections import defaultdict
paths = [ l.strip().split('-') for l in open('input12.txt') ]

cave = defaultdict(list)
for a,b in paths:
    cave[a].append(b)
    cave[b].append(a)

res = []

def already_small_cave(n):
    for i in range(1,len(n)):
        x = n[i]
        if x.islower() and x in n[:i]: return True
    return False

def explore(n):
    if n[-1] == 'end':
        res.append(n.copy())
    else:
        for x in cave[n[-1]]:
            if x == 'start': continue
            if x.islower() and x in n and already_small_cave(n): continue
            explore(n+[x])

explore(['start'])

# for x in res:
#     print(x)
print(len(res))
