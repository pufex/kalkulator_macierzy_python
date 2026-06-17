from algorithms.linear_systems import gauss_elimination as gs
from algorithms.linear_systems import jacobian as jb
import numpy as np

a = np.array([[4.0, -1.0, 1.0], [1.0, 5.0, -2.0],[2.0, 1.0, -4.0]])
b = np.array([[4.0], [4.0], [1.0]])

print(a, b, sep = "\n", end = "\n\n")
# print(gs(a, b))
print(jb(a, b))
