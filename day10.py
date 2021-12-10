lines = [ x.strip() for x in open('input10.txt') ]

ends = {
    '{': '}',
    '<': '>',
    '(': ')',
    '[': ']'
}

errors = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

fix = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}

res = 0
res2 = []
for l in lines:

    stack = []
    corrupt = False
    for c in l:
        if c in '([{<':
            stack.append(c)
        if c in ')]}>':
            e = stack.pop()
            if ends[e] != c:
                res += errors[c]
                corrupt = True
    if not corrupt:
        s = 0
        for c in reversed(stack):
            s *= 5
            s += fix[c]

        res2.append(s)

res2 = sorted(res2)

print(res)
print(res2[len(res2)//2])
