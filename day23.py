import re
from collections import defaultdict
from queue import PriorityQueue
from functools import cache

map = '''
#############
#12.3.4.5.67#
###8#A#C#E###
  #9#B#D#F#
  #########
'''

_links = [
    ( 1, 2, 1),
    ( 2, 3, 2),
    ( 2, 8, 2),
    ( 8, 9, 1),
    ( 8, 3, 2),
    ( 3,10, 2),
    ( 3, 4, 2),
    (10,11, 1),
    (10, 4, 2),
    ( 4,12, 2),
    ( 4, 5, 2),
    (12,13, 1),
    (12, 5, 2),
    ( 5,14, 2),
    ( 5, 6, 2),
    (14,15, 1),
    (14, 6, 2),
    ( 6, 7, 1)
]

links = defaultdict(dict)
for a,b,c in _links:
    links[a][b] = c
    links[b][a] = c

def find_paths(i):

    dist = {}
    dist[i] = 0
    q = dist.copy()
    prev = dict()
    prev[i] = None

    while q:
        e = min(q.items(), key=lambda x:x[1])[0]
        d = q.pop(e)
        dist[e] = d
        for b in links[e]:
            cost = d+links[e][b]
            if b not in prev and cost<q.get(b,1000):
                q[b] = cost
                prev[b] = e


    res = {}
    for j in range(1,16):
        if i == j: continue
        path = [j]
        e = j
        while e:
            e = prev[e]
            if e: path.append(e)

        res[j] = list(reversed(path)), dist[j]


    return res

paths = { i:find_paths(i) for i in range(1,16) }

energy = dict(A=1,B=10,C=100,D=1000)

slots = dict(A=[9,8], B=[11,10], C=[13,12], D=[15,14])


def show(types, pos, last):
    out = map.lower()
    for i in range(len(pos)):
        out = out.replace('%x'%pos[i], types[i])

    out = out.replace('%x'%last, '+')

    out = re.sub('[0-9a-f]','.', out)
    return out

def playback(types, pos, moves):
    pos = list(pos)
    total = 0
    for i, last, m, c in moves:
        pos[i] = m
        total += c
        print(last, m, paths[last][m],c)
        print(show(types, pos, last))

    print('total', total)

def possible_moves(types, pos, i):

    # i'm already at the back of my room
    if pos[i]>7 and pos[i] == slots[types[i]][0]: return []

    res = []
    for p,(path,cost) in paths[pos[i]].items():
        #print(f'considering {p} from {pos[i]}, {path} in {pos}')

        # do go into wrong room
        if p>7 and p not in slots[types[i]]: continue

        back, front = slots[types[i]]

        # don't take the front pos if the back is empty
        if p == front and back not in pos: continue

        # don't go into your room if it's blocking someone else
        if p == front and back in pos and types[pos.index(back)] != types[i] : continue

        # don't leave your room unless you are blocking someone else
        if p<8 and pos[i]>7 and pos[i] == front \
          and back in pos and types[pos.index(back)] == types[i]: continue

        # don't move around in the corridor
        if pos[i]<8 and p<8: continue

        if all(x not in pos for x in path[1:]):
            #print('it is good!')
            res.append((p,cost))

    return res

DEBUG = False

min_cost = 10000000
n = 0

@cache
def get_cost(types, pos, cost_so_far=0):
    global min_cost,n

    n = n+1
    if DEBUG: print(show(types, pos))

    if all(pos[i] in slots[types[i]] for i in range(len(pos))):
        if cost_so_far<min_cost:
            print(f"Found new min {cost_so_far} < {min_cost}")
            min_cost = cost_so_far
        #print('done!')
        #import ipdb; ipdb.set_trace()
        return [[]]

    res = []
    for i in range(len(pos)):
        for p,cost in possible_moves(types, pos, i):

            cost = energy[types[i]]*cost

            if min_cost<cost_so_far+cost: continue

            if DEBUG: print(i, types[i], pos[i], '->', p)
            pos_ = list(pos)
            pos_[i] = p
            res += [ [(i, pos[i], p, cost)] + m for m in get_cost(types, tuple(pos_), cost_so_far+cost) ]

    return res

# example
#types = 'AABBCCDD'
#pos = (9,15,8,12,10,13,11,14)

# mine:
#############
#...........#
###B#A#B#C###
  #C#D#D#A#
  #########
types = 'AABBCCDD'
pos = (10,15,8,12,9,14,11,13)

moves = get_cost(types, pos)
moves = [ (sum(x[3] for x in m),m) for m in moves ]
best = min(moves)

#best = ([(3, 12, 3), (4, 10, 4), (4, 4, 12), (6, 11, 4), (3, 3, 11), (2, 8, 3), (2, 3, 10), (7, 14, 5), (1, 15, 6), (7, 5, 15), (6, 4, 14), (1, 6, 8)], 11520)

playback(types, pos, best[1])

print(f"visited {n} states")
