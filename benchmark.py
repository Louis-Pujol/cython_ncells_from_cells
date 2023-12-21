from ncells_from_cells import python_ncells_from_cells, cython_ncells_from_cells
import numpy as np
from time import time


times_python = []
times_cython = []

n_faces_list = np.logspace(1, 7, 10, dtype=int)
for n_faces in n_faces_list:

    array = np.tile([3, 0, 1, 2], n_faces)
    start = time()
    assert python_ncells_from_cells(array) == n_faces
    end = time()
    times_python.append(end - start)

    start = time()
    assert cython_ncells_from_cells(array) == n_faces
    end = time()
    times_cython.append(end - start)

import matplotlib.pyplot as plt
plt.plot(n_faces_list, times_python, label='python')
plt.plot(n_faces_list, times_cython, label='cython')
plt.legend()
plt.xlabel('number of faces')
plt.ylabel('time (s)')
plt.xscale('log')
plt.show()

for i, n_faces in enumerate(n_faces_list):
    print(f'{n_faces} points: python: {times_python[i]:.3f} s, cython: {times_cython[i]:.3f} s, ratio: {times_python[i]/times_cython[i]:.3f}')