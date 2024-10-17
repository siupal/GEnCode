from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension("fast_operations", ["src/fast_operations.pyx"],
              include_dirs=[np.get_include()])
]

setup(
    name="EcoSyn",
    ext_modules=cythonize(extensions),
    include_dirs=[np.get_include()]
)
