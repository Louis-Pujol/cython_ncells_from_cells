import pytest
from ncells_from_cells import(
    python_ncells_from_cells,
    cython_ncells_from_cells,

)



def _test_ncells(f):
    
    valid_padding = [3, 0, 1, 2, 2, 1, 2, 4, 1, 2, 3, 8]
    assert f(valid_padding) == 3
    assert f([]) == 0
    assert f([1, 0]) == 1

    invalid_padding = [8, 0, 1, 2, 3, 4]
    with pytest.raises(ValueError):
        f(invalid_padding)

    invalid_padding = [3, 0, 1]
    with pytest.raises(ValueError):
        f(invalid_padding)

    invalid_padding = [3, 0]
    with pytest.raises(ValueError):
        f(invalid_padding)

    invalid_padding = [3]
    with pytest.raises(ValueError):
        f(invalid_padding)

def test_python_ncells_from_cells():
    _test_ncells(python_ncells_from_cells)

def test_cython_ncells_from_cells():
    _test_ncells(cython_ncells_from_cells)