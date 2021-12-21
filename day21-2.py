from collections import Counter
from functools import cache

positions = { 1:3, 2:7 }

def die(n):
    if len(n)==3: return Counter([sum(n)])

    res = Counter()
    res += die(n+[1])
    res += die(n+[2])
    res += die(n+[3])

    return res

rolls = die([])

print(rolls, len(rolls))

@cache
def wins(scores, pos, p):
    print(scores, pos, p)
    res = [0,0]
    for d in rolls:
        pos_ = list(pos)
        scores_ = list(scores)
        print(d)
        pos_[p] = (pos[p] + d) % 10
        scores_[p] += pos_[p] + 1
        if scores_[p]>=21:
            res[p] += rolls[d]
        else:
            r = wins(tuple(scores_), tuple(pos_), 0 if p else 1)
            res[0] += rolls[d]*r[0]
            res[1] += rolls[d]*r[1]
    print(res)
    return res

#print(wins((0,0),(3,7),0))

r = wins((0,0),(4,5),0)
print(r)
print(max(r))
