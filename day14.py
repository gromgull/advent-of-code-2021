from collections import Counter
from functools import cache

lines = [ l.strip() for l in open('input14.txt') ]
string = lines[0]
pairs = dict([ l.split(' -> ') for l in lines[2:] ])

# naive
# for i in range(10):
#     nxt = ''
#     for j in range(len(string)-1):
#         nxt += string[j] + pairs[string[j:j+2]]

#     nxt += string[-1]

#     string = nxt
#     #print(i, string)

# c = Counter(nxt)
# items = sorted(list(c.items()), key=lambda i: i[1])
# print(items[-1][1]-items[0][1])


@cache
def expand(s, n):
    #print(' '*n, s)
    if not n: return Counter(s)

    res = Counter()
    for i in range(len(s)-1):
        ins = pairs[s[i:i+2]]
        #print(' '*n, s[i:i+2], '->', ins)
        a = expand(s[i] + ins, n-1)
        b = expand(ins + s[i+1], n-1)
        #print(' '*n, '>', a,b)
        res += a + b
        res[ins] -= 1
        res[s[i+1]] -= 1

    res[s[-1]] += 1

    return res

# print(expand(lines[0], 1))
# print(Counter('NCNBCHB'))

# print(expand(lines[0], 2))
# print(Counter('NBCCNBBBCBHCB'))

c = expand(lines[0], 40)
items = sorted(list(c.items()), key=lambda i: i[1])
print(items[-1][1]-items[0][1])
