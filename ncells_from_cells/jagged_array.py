"""Jagged array implementation."""
from __future__ import annotations
from typing import Any
import numpy as np


class JaggedArray:
    """Array of variable length arrays.

    The jagged array is implemented as a wrapper around a VTK cell connectivity
    array and a cell offsets array. The cell offsets array is a 1d int array
    with the number of points per cell. The VTK cell connectivity array is a 1d
    int array with padding information.

    Parameters
    ----------
    connectivity_array : numpy.ndarray
        A VTK cell connectivity array (1d int array with padding information).
    offsets : numpy.ndarray
        A cell offsets array (1d int array with the number of points per cell).
    """

    def __init__(
            self: JaggedArray,
            connectivity_array: np.ndarray,
            offsets: np.ndarray,
            ) -> None:
        """Class constructor."""
        self._connectivity_array = connectivity_array.copy()
        self._offsets = offsets.copy()

        self.starts = np.zeros(self.n_cells, dtype=int)
        self.starts[1:] = (
            np.cumsum(offsets)[:-1]
            + np.arange(self.n_cells - 1, dtype=int)
            + 1
        )
        self.starts += 1
        self.end = self.starts + offsets

    def __getitem__(self: JaggedArray, i: int) -> np.ndarray:
        """Indexing operator."""
        if i >= self.n_cells:
            raise IndexError(
                f"Index {i} out of bounds for {self.n_cells} cells."
                )
        return self.connectivity_array[self.starts[i]: self.end[i]]

    def __len__(self: JaggedArray) -> int:
        """Length (number of cells) of the jagged array."""
        return self.n_cells

    # Define properties for the connectivity array and the offsets array
    # that raise an error when trying to set them (immutable)
    @property
    def connectivity_array(self: JaggedArray) -> np.ndarray:
        """The connectivity array."""
        return self._connectivity_array

    @connectivity_array.setter
    def connectivity_array(self: JaggedArray, value: Any) -> None:
        """Setter for connectivity array."""
        raise AttributeError("Cannot set connectivity array.")

    @property
    def offsets(self: JaggedArray) -> np.ndarray:
        """The offsets array."""
        return self._offsets

    @offsets.setter
    def offsets(self: JaggedArray, value: Any) -> None:
        """Offsets array setter."""
        raise AttributeError("Cannot set offsets array.")

    # Define a property for the number of cells
    @property
    def n_cells(self: JaggedArray) -> int:
        """The number of cells."""
        return len(self.offsets)
