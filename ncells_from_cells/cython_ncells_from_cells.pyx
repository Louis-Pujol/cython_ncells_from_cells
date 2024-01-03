# distutils: language = c++

cimport cython

from libc.math cimport sqrt
cimport numpy as cnp
cnp.import_array()
import numpy as np

INT_DTYPE = np.int64
ctypedef cnp.int64_t INT_DTYPE_t
from libcpp.vector cimport vector


def ncells_from_cells(INT_DTYPE_t [:] cells, int return_offsets=0):
    # Start from the beginning of the array
    cdef int position = 0
    cdef int length = len(cells)
    cdef int ncells = 0

    cdef INT_DTYPE_t[:] offsets = np.empty(length, dtype=INT_DTYPE)
    cdef int n_chunks = 0

    # While there remains elements to read
    while length > position:
        ncells += 1
        # Read the size of the next chunk of integers
        offset = cells[position]
        # Check is there are enough elements to read the chunk
        if position + offset >= length:
            raise ValueError(
                f"Array has invalid padding, the last chunk is expected to "
                f"be of size {offset}. Only {length - 1 - position} elements can be read."
            )
        # Store the offset
        offsets[n_chunks] = offset
        n_chunks += 1

        # Move to the next chunk
        position += offset + 1

    np.asarray(offsets, dtype=INT_DTYPE)
    if return_offsets == 0:
        return ncells
    else:
        return ncells, np.asarray(offsets[:n_chunks])