lst = [ x.split() for x in open("input2.txt") ]
lst = [ (x[0], int(x[1])) for x in lst ]

pos = sum([ x[1] for x in lst if x[0]=='forward'])
depth = sum([ x[1] for x in lst if x[0]=='up']) - sum([ x[1] for x in lst if x[0]=='down'])

print(pos, depth, pos*depth)

pos = 0
depth = 0
aim = 0

for cmd,arg in lst:
    match cmd:
        case 'forward':
            pos += arg
            depth += aim*arg
        case 'down':
            aim += arg
        case 'up':
            aim -= arg

print(pos,depth,aim,pos*depth)
