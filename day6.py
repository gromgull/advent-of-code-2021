from collections import Counter

fish = [ int(f) for f in next(open('input6.txt')).strip().split(',') ]

c = Counter(fish)
print(c)

for d in range(256):
    nc = Counter()
    for f,count in c.items():
        if f == 0:
            nc[8] += count
            nc[6] += count
        else:
            nc[f-1] += count
    c = nc

print(nc, sum(nc.values()))
