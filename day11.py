import numpy as np
from scipy.signal import convolve2d

a = np.array([list(l.strip()) for l in open('input11.txt')], dtype=int)

fltr = np.ones((3,3))

res = 0
for i in range(10000):
    # print(a)
    a += 1

    can_flash = np.ones(a.shape, dtype=bool)
    while True:
       last = np.copy(a)

       new_flash = (a>9) & (can_flash)

       can_flash[new_flash] = False
       res += new_flash.nonzero()[0].size
       new_flash = convolve2d(new_flash, fltr, mode='same').astype(int)

       a += new_flash

       if np.all(a == last): break

    if np.logical_not(can_flash).nonzero()[0].size == a.size:
        break
    a[np.logical_not(can_flash)] = 0

print(res)
print(i+1)
