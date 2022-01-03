from functools import cache
from itertools import product
from tqdm import tqdm

class Expr:

    def __init__(self, i, a, b=None):
        self.i = i
        self.a = a
        self.b = b

        self.cache = {}

    @cache
    def idx(self):
        a = set() if isinstance(self.a, int) else self.a.idx()
        b = set() if isinstance(self.b, int) else self.b.idx()
        return a.union(b)

    def evl(self, inputs):

        k = tuple(inputs[i] for i in self.idx())
        if k not in self.cache:
            a = self.a if isinstance(self.a, int) else self.a.evl(inputs)
            b = self.b if isinstance(self.b, int) else self.b.evl(inputs)
            self.cache[k] = self._evl(a,b,inputs)
        return self.cache[k]

    def __str__(self):
        a = self.a if isinstance(self.a, int) else f"[{self.a.i}]"
        b = self.b if isinstance(self.b, int) else f"[{self.b.i}]"
        return f"{self.__class__.__name__}({self.i}, {a}, {b})"

class Inp(Expr):
    def evl(self, inputs):
        return inputs[self.a]
    def idx(self):
        return set([self.a])
    def __str__(self):
        return f"Input({self.a})"

class Add(Expr):
    def _evl(self, a, b, inputs):
        return a+b
class Mul(Expr):
    def _evl(self, a, b, inputs):
        return a*b
class Div(Expr):
    def _evl(self, a, b, inputs):
        return a//b
class Mod(Expr):
    def _evl(self, a, b, inputs):
        return a%b
class Eql(Expr):
    def _evl(self, a, b, inputs):
        return 1 if a==b else 0

def compile(prog):
    regs = dict(w=0,x=0,y=0,z=0)
    inputs = [ Inp(-1, i) for i in range(14) ]
    for i,(inst, a, *b) in enumerate(prog):
        b = b[0] if b else None
        print(i,inst,a,b)
        match inst:
            case "inp":
                regs[a] = inputs.pop(0)
            case "add":
                regs[a] = Add(i, regs.get(a,a), regs.get(b,b))
            case "mul":
                regs[a] = Mul(i, regs.get(a,a), regs.get(b,b))
            case "div":
                regs[a] = Div(i, regs.get(a,a), regs.get(b,b))
            case "mod":
                regs[a] = Mod(i, regs.get(a,a), regs.get(b,b))
            case "eql":
                regs[a] = Eql(i, regs.get(a,a), regs.get(b,b))
        #print(regs[a])
    return regs['z']

prog = [ line.strip().split(' ') for line in open('input24.txt') ]
prog = [ [ line[0] ] + [ int(x) if x not in 'wxyz' else x for x in line[1:]] for line in prog ]

p = compile(prog)

q = [p]
seen = set()
while q:
    e = q.pop(0)
    if isinstance(e, int): continue
    if e in seen:
        print(f"Already saw {e}")
        continue
    seen.add(e)
    q.append(e.a)
    if e.b: q.append(e.b)

print(p.idx())

for o in sorted(seen, key=lambda o: o.i):
    print(o, o.idx())

def model_numbers():
    yield from product(*(range(9,0,-1) for _ in range(14)))

# for m in tqdm(model_numbers()):
#     if not p.evl(m):
#         print(m)
#         break

print(p.evl(tuple([int(x) for x in '13579246899999'])))
