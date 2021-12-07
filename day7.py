import numpy as np

crabs = np.array(next(open('input7.txt')).strip().split(','), dtype=int)

a = np.arange(crabs.min(), crabs.max()+1)

res = [ np.abs(crabs-x).sum() for x in a ]

m = np.argmin(res)

print(res, m, res[m])

res = [ np.abs(crabs-x) for x in a ]
res = [ (x*(x+1)//2).sum() for x in res ]

m = np.argmin(res)

print(res, m, res[m])
