from .cython_ncells_from_cells import ncells_from_cells as _cython_ncells_from_cells


from collections import deque
from itertools import count, islice
import numpy as np

def cython_ncells_from_cells(cells) -> int:
    """Get the number of cells from a VTK cell connectivity array.

    Parameters
    ----------
    cells : numpy.ndarray
        A VTK cell connectivity array.

    Returns
    -------
    int
        The number of cells extracted from the given cell connectivity array.

    """
    cells = np.ascontiguousarray(cells).astype(np.int64)
    return _cython_ncells_from_cells(cells)

def python_ncells_from_cells(cells) -> int:
    """Get the number of cells from a VTK cell connectivity array.

    Parameters
    ----------
    cells : numpy.ndarray
        A VTK cell connectivity array.

    Returns
    -------
    int
        The number of cells extracted from the given cell connectivity array.

    """
    cells = np.ascontiguousarray(cells).astype(np.int64)
    consumer = deque(maxlen=0)
    it = cells.flat
    expected_length = 0
    actual_length = len(cells)
    counter = 0
    for n_cells in count():  # noqa: B007
        skip = next(it, None)
        if skip is None:
            break
        counter += skip + 1
        last_skip = skip
        consumer.extend(islice(it, skip))  # type: ignore
        expected_length += skip + 1

    if actual_length != expected_length:
        lastchunk_size = last_skip - (expected_length - actual_length)
        raise ValueError(
                f"Array has invalid padding, the last chunk is expected to "
                f"be of size {last_skip}. Only {lastchunk_size} elements can be read."
            )
    return n_cells