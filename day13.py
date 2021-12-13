import numpy as np
import re

data = [ x.strip() for x in open('input13.txt') ]
i = data.index('')

xys = [ l.split(',') for l in data[:i] ]
folds = [ l.replace('fold along ', '').split('=') for l in data[i+1:]]
folds = [ (l[0],int(l[1])) for l in folds ]

xs = np.array([ int(l[0]) for l in xys ])
ys = np.array([ int(l[1]) for l in xys ])

paper = np.zeros((xs.max()+1, ys.max()+1),dtype=bool)

paper[xs,ys] = 1

print(paper.astype(int))

for axis,fold in folds:
    print(paper.shape)
    print(axis,fold)
    if axis=='y':
        a = paper[:,:fold]
        b = paper[:,fold+1:][:,::-1]
        paper = a
        paper[:,-b.shape[1]:] |= b
    elif axis=='x':
        a = paper[:fold,:]
        b = paper[fold+1:,:][::-1,:]
        paper = a
        paper[-b.shape[0]:,:] |= b

msg = str(paper.astype(int).T)
msg = re.sub(r'([^\]])\n',r'\1', msg)
msg = re.sub(r'0[ \]]',' ', msg)
msg = re.sub(r'1[ \]]','*', msg)

print(msg)

print(paper.nonzero()[0].size)
