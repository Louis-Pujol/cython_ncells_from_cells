"""Test to convert a connectivity array to a jagged array."""

import numpy as np
import pytest

from ncells_from_cells import to_jagged_array


def test_jagged_array() -> None:
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

    jagged_array = to_jagged_array(cells)

    assert len(jagged_array) == len(list_cells)
    for i in range(len(jagged_array)):
        assert np.allclose(jagged_array[i], list_cells[i])

    # Try to catch some errors
    with pytest.raises(IndexError):  # Index out of bounds
        jagged_array[len(jagged_array)]

    with pytest.raises(AttributeError):  # Connectivity array is immutable
        jagged_array.connectivity_array = np.array([0, 1, 2])

    with pytest.raises(AttributeError):  # Offsets array is immutable
        jagged_array.offsets = np.array([0, 1, 2])
