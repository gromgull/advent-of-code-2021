import math

class NoActionException(Exception): pass

def nextnum(s,i,d=1):
    while True and i>=0 and i<len(s):
        if isinstance(s[i], int): return i
        i += d

def lastnum(s,i): return nextnum(s,i,-1)

def action(s):

    depth = 0
    for i in range(len(s)):
        # explodes
        c = s[i]
        if c == '[': depth += 1
        if c == ']': depth -= 1

        if depth > 4 and isinstance(s[i], int) and isinstance(s[i+1], int):
            if j := lastnum(s,i-1):
                s[j] += s[i]
            if j := nextnum(s,i+2):
                s[j] += s[i+1]
            s[i-1:i+3] = [0]
            return s

    for i in range(len(s)):
        # splits

        if isinstance(s[i], int) and s[i]>9:
            n = s[i] / 2
            s[i:i+1] = ['[', int(math.floor(n)), int(math.ceil(n)), ']']
            return s

    raise NoActionException()

def reduce(s, it=-1):

    i = 0
    while True:
        try:
            s = action(s)
        except NoActionException:
            break
        i += 1
        if i == it: break

    return s

def add(a,b):
    return reduce(['['] + a + b + [']'])

def parse(s):
    return [ c if c in '[]' else int(c) for c in s if c != ',' ]

def process(s, it=1):
    return reduce(parse(s),it)

def to_list(s):
     stack = [[]]
     for c in s:
         if c == '[':
             stack.append([])
         elif c == ']':
             v = stack.pop()
             stack[-1].append(v)
         else:
             stack[-1].append(c)
     return stack.pop().pop()

def tostr(s):
    return str(to_list(s))

def test(a,b,it=1):
    a = to_list(process(a,it))
    b = eval(b)
    if a!=b:

        print(a,"!=",b)
        assert a==b

def add_all(lines):
    while len(lines)>1:
        print(tostr(lines[0]))
        print('+')
        print(tostr(lines[1]))
        lines = [add(lines[0], lines[1])] + lines[2:]
        print('=', tostr(lines[0]))
    return lines[0]


def magnitude(s):
    s = to_list(s)

    def _m(s):
        if isinstance(s, int): return s
        return _m(3*_m(s[0])+2*_m(s[1]))

    return _m(s)

# explode
test('[[[[[9,8],1],2],3],4]', '[[[[0,9],2],3],4]')
test('[7,[6,[5,[4,[3,2]]]]]', '[7,[6,[5,[7,0]]]]')
test('[[6,[5,[4,[3,2]]]],1]','[[6,[5,[7,0]]],3]')
test('[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]', '[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]')
test('[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]','[[3,[2,[8,0]]],[9,[5,[7,0]]]]')

# split
test('[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]', '[[[[0,7],4],[[7,8],[6,0]]],[8,1]]', -1)

# add
print(tostr(add_all([parse(l) for l in ['[1,1]', '[2,2]', '[3,3]', '[4,4]', '[5,5]' ]])))
print(tostr(add_all([parse(l) for l in ['[1,1]', '[2,2]', '[3,3]', '[4,4]', '[5,5]', '[6,6]' ]])))

lines = [ parse(l.strip()) for l in open('input18.txt') ]
lines2 = lines.copy()
res = add_all(lines)

print(tostr(res))
print(magnitude(res))

largest = -1
for l1 in lines2:
    for l2 in lines2:
        m = magnitude(add(l1,l2))
        if m>largest: largest = m

print(largest)
