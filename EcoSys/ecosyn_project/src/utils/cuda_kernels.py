import pycuda.driver as cuda
from pycuda.compiler import SourceModule

cuda_code = """
__global__ void update_environment(float *temperature, float *humidity, float *light_intensity, 
                                   float *soil_fertility, int width, int height, float time_step)
{
    int idx = blockIdx.x * blockDim.x + threadIdx.x;
    int idy = blockIdx.y * blockDim.y + threadIdx.y;
    int index = idy * width + idx;

    if (idx < width && idy < height) {
        temperature[index] += -1.0f + 2.0f * (float)rand() / RAND_MAX;
        humidity[index] = fmaxf(0.0f, fminf(humidity[index] + -5.0f + 10.0f * (float)rand() / RAND_MAX, 100.0f));
        light_intensity[index] = fmaxf(0.0f, fminf(light_intensity[index] + -5.0f + 10.0f * (float)rand() / RAND_MAX, 100.0f));
        soil_fertility[index] = fmaxf(0.0f, fminf(soil_fertility[index] + -0.1f + 0.2f * (float)rand() / RAND_MAX, 10.0f));
    }
}
"""

mod = SourceModule(cuda_code)
update_environment_kernel = mod.get_function("update_environment")