# cython: language_level=3
import cython
import numpy as np
cimport numpy as np

@cython.boundscheck(False)
@cython.wraparound(False)
def update_environment(double[:, :] temperature, double[:, :] humidity, double[:, :] light_intensity, double[:, :] soil_fertility):
    cdef int height = temperature.shape[0]
    cdef int width = temperature.shape[1]
    cdef int x, y
    cdef double noise

    for y in range(height):
        for x in range(width):
            noise = np.random.normal(0, 0.1)
            temperature[y, x] += noise
            humidity[y, x] = max(0, min(100, humidity[y, x] + np.random.normal(0, 0.5)))
            light_intensity[y, x] = max(0, min(200, light_intensity[y, x] + np.random.normal(0, 1.0)))
            soil_fertility[y, x] = max(0, min(10, soil_fertility[y, x] + np.random.normal(0, 0.1)))
