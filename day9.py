import numpy as np
a = np.array( [ list(l.strip()) for l in open('input9.txt') ], dtype=int)

print(a)
edge = np.ones((a.shape[0],1), dtype=bool)
left = np.hstack(((a[:,:-1]-a[:,1:])<0, edge))
right = np.hstack((edge, (a[:,1:]-a[:,:-1])<0))

edge = np.ones((1,a.shape[1]), dtype=bool)
below = np.vstack(((a[:-1,:]-a[1:,:])<0, edge))
above = np.vstack((edge, (a[1:,:]-a[:-1,:])<0))


print(left.astype(int))
print(right.astype(int))
print(below.astype(int))
print(above.astype(int))

low = left & right & above & below

print(low.astype(int))

print((a[low]+1).sum())

idx = np.where(low)
basin = 0-np.arange(idx[0].size)-1
nines = a==9

while True:

    last = np.copy(a)

    a[idx] = basin
    a[nines] = 9

    # why didn't I use convolve2d for this? :thinking_face:
    idx = (np.concatenate((idx[0]+1, idx[0]-1, idx[0], idx[0])), np.concatenate((idx[1], idx[1], idx[1]+1, idx[1]-1)))
    basin = np.concatenate((basin, basin, basin, basin))

    oob = (idx[0]>=0) & (idx[0]<a.shape[0]) & (idx[1]>=0) & (idx[1]<a.shape[1])
    basin = basin[oob]
    idx = (idx[0][oob], idx[1][oob])

    ok = (a[idx] != 9) & (a[idx]>=0)
    basin = basin[ok]
    idx = idx[0][ok], idx[1][ok]

    if np.all(last == a): break

print(a)
basins = sorted([ (a==-(v+1)).nonzero()[0].size for v in range(low.nonzero()[0].size) ])
print(basins[-3:], np.prod(basins[-3:]))
