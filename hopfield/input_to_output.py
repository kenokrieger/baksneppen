import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    fig = plt.figure()
    fig.suptitle("Memorisation process in the Hopfield Model")

    for idx in range(9):
        ax = plt.subplot(int(f"33{idx + 1}"))
        ax.set_axis_off()
        image = np.loadtxt("progress/step_{}{}.dat".format(idx, "0" * 4 if idx else ""))
        ax.imshow(image, cmap="binary", aspect="equal")

    plt.tight_layout()
    plt.savefig("result.png")
