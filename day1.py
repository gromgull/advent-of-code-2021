import numpy as np
lst = np.array([ int(x) for x in open('input1.txt') ])

print(((lst[:-1]-lst[1:])<0).nonzero()[0].shape)

w = np.convolve(lst, [1,1,1])[2:-2]

print(((w[:-1]-w[1:])<0).nonzero()[0].shape)
