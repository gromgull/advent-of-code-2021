import numpy as np

lst = np.array([list(x.strip()) for x in open('input3.txt')]).astype(int)

def count(lst):
    return (lst.sum(axis=0)>=lst.shape[0]/2).astype('b')

bin = count(lst)

def dec(bin):
    return sum(bin*2**(np.arange(bin.shape[0],0, -1)-1))

a = dec(bin)
b = dec(np.logical_not(bin))

print(a,b,a*b)

def fltr(lst, nt):
    for i in range(lst.shape[1]):
        bin = count(lst)
        if nt: bin = np.logical_not(bin)
        lst = lst[ [ x[i] == bin[i] for x in lst ]]

        if lst.shape[0] == 1: return lst[0]

a = dec(fltr(lst, False))
b = dec(fltr(lst, True))

print(a,b,a*b)
