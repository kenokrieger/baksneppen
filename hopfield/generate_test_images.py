import numpy as np

test_images = ["memory/house.dat", "memory/painting.dat", "memory/street.dat"]


for image in test_images:
    arr = np.loadtxt(image)
    arr[25:, :] = 0
    arr[:, 25:] = 0
    np.savetxt(image.replace("memory", "tests"), arr, fmt="%i")


for image in test_images:
    arr = np.loadtxt(image)
    # randomly flip bits
    arr *= 1 - 2 * (np.random.randint(0, 4, size=arr.shape) // 3)
    np.savetxt(image.replace("memory/", "tests/noise_"), arr, fmt="%i")
