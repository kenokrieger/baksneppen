from sys import argv
import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    img = np.loadtxt(argv[1])
    plt.imshow(img, cmap="binary")
    plt.savefig(argv[1].replace(".dat", ".png"))
    plt.show()
