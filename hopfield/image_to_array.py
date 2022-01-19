import numpy as np
import matplotlib.image as mpimg
from sys import argv


def parse(img):
    array = mpimg.imread(img)
    array[np.where(array <= np.mean(array))] = -1
    array[np.where(array > np.mean(array))] = 1
    return array


if __name__ == "__main__":
    np.savetxt(argv[1].replace(".png", ".dat"), parse(argv[1]),fmt='%i')
