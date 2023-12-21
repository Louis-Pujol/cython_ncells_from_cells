# cython_ncells_from_cells
Try to speedup ncells_from_cells function from PyVista with Cython and raise a ValueError if the array is not valid with respect to the padding information

To install

```
pip install -e .
```

To run benchmark

```
pip install matplotlib
python benchmark.py
```

To test
```
pip install pytest
pytest tests/
```

For triangles faces with more than `1e5` faces, cython seems tp be `~5x` faster

()[benchmark.png]

```
10 points: python: 0.000 s, cython: 0.000 s, ratio: 3.689
46 points: python: 0.000 s, cython: 0.000 s, ratio: 7.424
215 points: python: 0.000 s, cython: 0.000 s, ratio: 7.635
1000 points: python: 0.001 s, cython: 0.000 s, ratio: 7.946
4641 points: python: 0.005 s, cython: 0.001 s, ratio: 7.908
21544 points: python: 0.012 s, cython: 0.002 s, ratio: 5.996
100000 points: python: 0.051 s, cython: 0.010 s, ratio: 5.406
464158 points: python: 0.233 s, cython: 0.041 s, ratio: 5.701
2154434 points: python: 1.083 s, cython: 0.189 s, ratio: 5.732
10000000 points: python: 5.019 s, cython: 0.869 s, ratio: 5.776
```