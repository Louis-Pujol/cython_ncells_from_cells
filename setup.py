from setuptools import setup, Extension
import numpy as np
from Cython.Build import cythonize

extension = Extension(
    name="ncells_from_cells.cython_ncells_from_cells",
    sources=[
        "ncells_from_cells/cython_ncells_from_cells.pyx",
    ],
    include_dirs=[np.get_include()],
    define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
)

dependencies = [
    "numpy",
    "pyvista @ git+https://github.com/pyvista/pyvista@main"

]

setup(
    name="ncells_from_cells",
    version="1.0",
    description="",
    author="Louis Pujol",
    author_email="",
    url="",
    install_requires=dependencies,
    ext_modules=cythonize([extension]),
)
