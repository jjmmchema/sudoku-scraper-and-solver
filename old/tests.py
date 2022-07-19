from functools import reduce
import os
from pprint import pprint
import numpy as np


arr1 = np.array([[1, 2, 3, 4],
          [1, 2, 3, 4],
          [1, 2, 3, 4],
          [1, 2, 3, 4],], dtype=np.int)

arr2 = np.random.randint(1, 10, (3, 3), dtype=np.int)

# with open("src/sudoku.txt", "r") as f:
#     for line in f.readlines():
#         t = list(map(lambda s: s.replace("-", ""), line.split(",")[:-1]))
#         pprint(t)


a = set(np.array([6, 8, 9, 3, 1, 5, 7]))
b = set(np.array([8, 1, 3, 4, 2]))
c = set(np.array([5, 1, 6, 7]))

# print(np.setdiff1d(a, b))
# print(np.setdiff1d(b, a))
# d  = set(a) ^ set(b)
# print(d ^ set(c))

l = [a, b, c]
# l = [set(t.tolist()) for t in l]
e = set.union(*l) - set.intersection(*l)
print(e)

# The XOR of the sets minus the AND of the sets
diff = (a ^ b ^ c) - (a & b & c) 
print(np.array(list(diff)))

# return list(set(posible_values).difference(arr))
# available_values = list(set(available_row_vals).intersection(available_column_vals))

f = [6, 8, 9, 3, 1, 5, 7]
g = [8, 1, 3, 4, 2]
h = [5, 1, 6, 7]
print(np.intersect1d(f, g))
print(np.intersect1d(g, f))

intersec = np.intersect1d(np.intersect1d(f, g), h)

print(set(f) & set(g) & set(h))
print(intersec)