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
    for i, last, m in moves:
        pos[i] = m
        c = paths[last][m][1]*energy[types[i]]
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

@cache
def get_cost(types, pos, moves=(), min_cost=10000000000):
    if DEBUG: print(show(types, pos, moves[-1][0][1] if moves else -1))

    cost_so_far = sum(x[1] for x in moves)

    if all(pos[i] in slots[types[i]] for i in range(len(pos))):
        #print('done!')
        #import ipdb; ipdb.set_trace()
        return (([x[0] for x in moves], cost_so_far),)

    res = ()
    for i in range(len(pos)):
        for p,cost in possible_moves(types, pos, i):

            if min_cost<cost_so_far+cost: continue

            if DEBUG: print(i, types[i], pos[i], '->', p)
            pos_ = list(pos)
            pos_[i] = p
            res += get_cost(types, tuple(pos_), moves+(((i,pos[i],p), cost*energy[types[i]]),), min_cost)

            if res:
                new_min_cost = min(res, key=lambda x: x[1])
                if new_min_cost[1]<min_cost:
                    print(p)
                    print(f"Found new min {new_min_cost[1]} ({min_cost}): {new_min_cost[0]}")
                    min_cost = new_min_cost[1]


    return res

# example
# moves = get_cost('AABBCCDD',
#                  (9,15,8,12,10,13,11,14))

# mine:
#############
#...........#
###B#A#B#C###
  #C#D#D#A#
  #########
moves = get_cost('AABBCCDD',
                  (10,15,8,12,9,14,11,13))

best = min(moves, key=lambda x: x[1])

#best = ([(3, 12, 3), (4, 10, 4), (4, 4, 12), (6, 11, 4), (3, 3, 11), (2, 8, 3), (2, 3, 10), (7, 14, 5), (1, 15, 6), (7, 5, 15), (6, 4, 14), (1, 6, 8)], 11520)

playback('AABBCCDD',
         (9,15,8,12,10,13,11,14), best[0])
