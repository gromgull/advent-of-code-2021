from itertools import cycle
from collections import defaultdict
scores = defaultdict(int)
positions = { 1:3, 2: 7 }
#positions = { 1:4, 2: 5 }
rolls = 0
die = cycle(range(100))
while True:
    for p in positions:
        roll = 3 + next(die) + next(die) + next(die)
        rolls += 3
        positions[p] = (positions[p] + roll) % 10
        scores[p] += positions[p] +1
        if scores[p]>=1000: break
    else:
        continue
    break

print(scores,rolls)
