from scipy.optimize import curve_fit
import numpy as np

import matplotlib.pyplot as plt

from uncertainties import ufloat

LOG_BINS = 30


def lin_func(x, a, b):
    return a * x + b

def power_law(x, a, b):
    return b * x ** a

if __name__ == "__main__":
    avalanches = np.loadtxt("avalanche_sizes.dat")

    fig = plt.figure()
    ax = fig.add_subplot(111)


    counts, bin_edges = np.histogram(avalanches + 1, bins=np.logspace(0, np.log10(np.max(avalanches)), LOG_BINS))
    counts = counts / np.diff(bin_edges)
    bin_centres = np.sqrt(bin_edges[1:] * bin_edges[:-1])

    params, pcov = curve_fit(lin_func, np.log(bin_centres), np.log(counts + 1))
    perr = np.sqrt(np.diag(pcov))
    ax.bar(bin_centres, counts, width=np.diff(bin_edges))

    ax.plot(bin_centres, power_law(bin_centres, -1.5, 10 ** 3), zorder=1, color="red")

    ax.set_title("Linearised avalanche distribution\nt = 100.000, n = 64x64")
    ax.set_xlabel("Avalanche duration")
    ax.set_ylabel("Frequency")
    ax.set_xscale("log")
    ax.set_yscale("log")
    a, b = ufloat(params[0], perr[0]), ufloat(params[1], perr[1])
    print(a, b)

    textstr = '\n'.join((
        "$f(x) = ax + b$",
        "$a = -1.5$",
        "$b = 3$",
    ))

    props = dict(boxstyle='round', alpha=1, color="darkgrey")

    ax.text(0.60, 0.95, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props)
    plt.savefig("power_law.png", dpi=200)
    plt.show()
