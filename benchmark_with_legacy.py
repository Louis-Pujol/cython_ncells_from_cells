import vtk

import numpy as np
from ncells_from_cells import cython_ncells_from_cells
from vtk import vtkCellArray
from pyvista.core.utilities import numpy_to_idarr
from pyvista.core.utilities import ncells_from_cells as pv_ncells_from_cells
from pyvista.core._vtk_core import vtk_to_numpy

def generate_random_cells(n_cells: int) -> np.ndarray:
    """Generate a random array of cells."""
    offsets = np.random.randint(1, 4, n_cells)
    cells = np.random.randint(0, 10, offsets.sum() + n_cells, dtype=np.int64)
    pos_offsetts = np.concatenate([[0],np.cumsum(offsets + 1)[: -1]])

    cells[pos_offsetts] = offsets

    return cells

n_cellss = [int(10**i) for i in np.linspace(4, 8, 10)]

times_pv = []
times_cython = []
times_legacy = []

for n_cells in n_cellss:
    print(f"n_cells: {n_cells}")

    cells = generate_random_cells(n_cells)
    vtk_idarr, cells = numpy_to_idarr(cells, deep=True, return_ind=True)  # type: ignore

    cellArray_pv = vtkCellArray()
    cellArray_cython = vtkCellArray()
    cellArray_legacy = vtkCellArray()

    from time import time

    # With Pyvista
    start = time()
    n_cells = pv_ncells_from_cells(cells)
    cellArray_pv.SetCells(n_cells, vtk_idarr)
    end = time()
    times_pv.append(end - start)


    # With Cython
    start = time()
    n_cells = cython_ncells_from_cells(cells)
    cellArray_cython.SetCells(n_cells, vtk_idarr)
    end = time()
    times_cython.append(end - start)

    # Using ImportLegacyFormat
    start = time()
    cellArray_legacy.ImportLegacyFormat(vtk_idarr)
    end = time()
    times_legacy.append(end - start)

    # Check that the results are the same
    assert np.allclose(cellArray_cython.GetNumberOfCells(), cellArray_legacy.GetNumberOfCells())
    assert np.allclose(cellArray_pv.GetNumberOfCells(), cellArray_legacy.GetNumberOfCells())
    assert np.allclose(cellArray_cython.GetConnectivityArray(), cellArray_legacy.GetConnectivityArray())
    assert np.allclose(cellArray_pv.GetConnectivityArray(), cellArray_legacy.GetConnectivityArray())

import matplotlib.pyplot as plt

plt.figure(figsize=(15, 15))
plt.plot(n_cellss, times_pv, label="pyvista")
plt.plot(n_cellss, times_cython, label="cython")
plt.plot(n_cellss, times_legacy, label="legacy")

plt.legend()
plt.xlabel("number of cells")
plt.ylabel("time to create CellArray (s)")
plt.xscale("log")
plt.show()