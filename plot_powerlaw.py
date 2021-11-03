from scipy.optimize import curve_fit
import numpy as np

import matplotlib.pyplot as plt

from uncertainties import ufloat

BINS = np.arange(0, 6, 0.3)


def linfunc(x, a, b):
    return a * x + b


if __name__ == "__main__":
    avalanches = np.loadtxt("avalanche_durations.dat")

    fig = plt.figure()
    ax = fig.add_subplot(111)

    count, _ = np.histogram(avalanches, BINS)
    nonzero_bins = BINS[np.nonzero(count)]
    nonzero_count = count[np.nonzero(count)]

    params, pcov = curve_fit(linfunc, nonzero_bins[8:], np.log10(nonzero_count[8:]))
    perr = np.sqrt(np.diag(pcov))
    ax.bar(nonzero_bins, np.log10(nonzero_count))
    ax.plot(nonzero_bins[8:] + 0.15, linfunc(nonzero_bins[8:], *params), zorder=1, color="red")

    ax.set_title("Linearised avalanche distribution\nt = 1.000.000, n = 100")
    ax.set_xlabel("Avalanche duration as log10")
    ax.set_ylabel("Frequency as log10")
    ax.set_xlim(-0.5, 7)
    a, b = ufloat(params[0], perr[0]), ufloat(params[1], perr[1])
    print(a, b)

    textstr = '\n'.join((
        "$f(x) = ax + b$",
        "$a = {}$".format(str(a).replace("+/-", "\\pm ")),
        "$b = {}$".format(str(b).replace("+/-", "\\pm ")),
    ))

    props = dict(boxstyle='round', alpha=1, color="darkgrey")

    ax.text(0.60, 0.95, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props)
    plt.savefig("power_law.png", dpi=200)
