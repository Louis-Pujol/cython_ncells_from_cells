"""Test to convert a connectivity array to a jagged array."""

import numpy as np
import pyvista as pv
import pytest

from ncells_from_cells import to_jagged_array


def test_irregular_cells() -> None:
    """Test to convert a connectivity array to a jagged array."""
    cells = np.array([2, 0, 1, 3, 6, 5, 4, 4, 2, 3, 1, 0, 1, 0, 1, 2, 2, 5, 6])
    list_cells = [
        [0, 1],
        [6, 5, 4],
        [2, 3, 1, 0],
        [0],
        [2],
        [5, 6],
    ]

    irregular_cells = to_jagged_array(cells)

    # irregular_cells has the same length as list_cells
    assert len(irregular_cells) == len(list_cells)
    # the elements of irregular_cells correspond to the individual cells
    for i in range(len(irregular_cells)):
        assert np.allclose(irregular_cells[i], list_cells[i])
    # irregular_cells can be used to create a PolyData object
    # thanks to the from_irregular_faces method
    mesh = pv.PolyData.from_irregular_faces(
        points=np.random.rand(10, 3),
        faces=irregular_cells,
    )
    assert np.allclose(mesh.faces, cells)

    

    # Try to catch some errors
    with pytest.raises(IndexError):  # Index out of bounds
        irregular_cells[len(irregular_cells)]

    with pytest.raises(AttributeError):  # Connectivity array is immutable
        irregular_cells.connectivity_array = np.array([0, 1, 2])

    with pytest.raises(AttributeError):  # Offsets array is immutable
        irregular_cells.offsets = np.array([0, 1, 2])

