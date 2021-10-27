from scipy.optimize import curve_fit
import numpy as np

import matplotlib.pyplot as plt

BINS = np.arange(0, 5, 1)


def linfunc(x, a, b):
    return a * x + b


if __name__ == "__main__":
    avalanches = np.loadtxt("avalanche_durations.dat")
    count, _ = np.histogram(avalanches, BINS)
    params, pcov = curve_fit(linfunc, BINS[:-1], np.log10(count))
    plt.plot(BINS[:-1], np.exp(linfunc(BINS[:-1], *params)))
    plt.yscale("log")
    print(params[0])
    plt.show()
