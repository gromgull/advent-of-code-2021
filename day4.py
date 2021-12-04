import numpy as np

lst = [x.strip() for x in open('input4.txt')]

draws = [int(x) for x in lst[0].split(',')]
lst = lst[2:]

boards = np.array([ [ line.split() for line in lst[x:x+5]]
          for x in range(0,len(lst),6) ]).astype('i')

# print(draws)
# print(boards)

hasnt_won = np.ones(boards.shape[0], dtype=bool)
wins = []
scores = []

for i in range(len(draws)):

    drawn = np.vectorize(lambda x: x in draws[:i])(boards)

    idx = drawn.all(axis=2).any(axis=1) | drawn.all(axis=1).any(axis=1)
    wins.append(boards[idx & hasnt_won])

    scores.append(wins[-1][np.logical_not(drawn[idx & hasnt_won])].sum(axis=0))
    hasnt_won[idx] = False

first = None
for i in range(len(draws)):
    if wins[i].size:
        if first is None: first = i
        last = i


print(first, wins[first], draws[first-1], scores[first], scores[first]*draws[first-1])
print(last, wins[last], draws[last-1], scores[last], scores[last]*draws[last-1])
