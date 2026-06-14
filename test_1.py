from algorithms.linear_systems import gauss_elimination as gs
import numpy as np

a = np.array([[2.0, 1.0, 1.0],[1.0, 3.0, 2.0],[1.0, 1.0, 4.0]])
b = np.array([[4.0], [9.0], [6.0]])

print(a, b, sep = "\n", end = "\n\n")
print(gs(a, b))
