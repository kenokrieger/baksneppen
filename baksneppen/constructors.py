import numpy as np

import tkinter as tk

import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker

HIST_BINS = np.arange(0, 7, 1)

PLOTS = {
    "fitness": {
        "title": "Fitness of the species",
        "xlabel": "Position in array",
        "ylabel": "Fitness"
    },
    "fitness change": {
        "title": "Change in minimum fitness",
        "xlabel": "time",
        "ylabel": "Change"
    },
    "avalanche durations": {
        "title": "Histogram of avalanche durations",
        "xlabel": "Duration",
        "ylabel": "Frequency"
    }
}


def add_subplots(figure):
    """
    Add subplots to a figure to visualise the dynamic of the Bak-Sneppen
    evolution model.

    Args:
        figure(matplotlib.pyplot.Figure): The figure to add the subplots to.

    Returns:
        dict: The created axes.

    """
    axes = dict()
    grid = gridspec.GridSpec(ncols=2, nrows=2, figure=figure)
    axes["fitness"] = figure.add_subplot(grid[0:, 0])
    axes["fitness change"] = figure.add_subplot(grid[0, 1])
    axes["avalanche durations"] = figure.add_subplot(grid[1, 1])

    for plot in PLOTS:
        axes[plot].set_title(PLOTS[plot]["title"])
        axes[plot].set_xlabel(PLOTS[plot]["xlabel"])
        axes[plot].set_ylabel(PLOTS[plot]["ylabel"])

    axes["avalanche durations"].xaxis.set_major_formatter(
        ticker.FormatStrFormatter("$10^%d$")
    )
    axes["fitness"].set_ylim(0, 1.0)

    figure.tight_layout()

    return axes


def add_artists(axes):
    """
    Add lines and barplots to a figure and the specified axes.

    Args:
        axes(dict): The axes to add the artists to.

    Returns:
        tuple: The added lines and bars sorted in two dictionaries.

    """
    # all objects that can be updated with the 'set_data'-method
    lines = dict()
    # all objects that can be updated by resizing rectangles
    bars = dict()
    lines["scatter"], = axes["fitness"].plot([], [], color="blue", marker="o",
                                             linewidth=0)
    lines["least fitness"], = axes["fitness"].plot([], [], color="blue",
                                                   linestyle="dashed")

    lines["fitness change"], = axes["fitness change"].plot([], [], color="blue")

    _, _, bars["duration histogram"] = axes["avalanche durations"].hist(
        [0.01], HIST_BINS, rwidth=0.9
    )
    return lines, bars


def update_artists(artists, data):
    """
    Update the artists and axes to display the given data.

    Args:
        artists(tuple): The lines and bars to update.
        data(dict): The data to display on the lines and bars

    Returns:
        None.

    """
    lines, bars = artists
    nspecies = np.arange(0, data["species"].shape[0], 1)
    lines["scatter"].set_data(nspecies, data["species"])
    lines["least fitness"].set_data(nspecies, data["fitness over time"][-1])
    lines["fitness change"].set_data(
        np.arange(0, data["fitness over time"].shape[0], 1),
        np.array(data["fitness over time"])
    )

    n, _ = np.histogram(data["avalanche durations"], HIST_BINS)
    for count, rect in zip(n, bars["duration histogram"]):
        rect.set_height(count)


def update_axes(axes, data):
    """
    """
    axes["fitness"].set_xlim(-0.3, data["system size"] - 0.7)
    axes["fitness change"].set_xlim(0, data["time"])
    axes["fitness change"].set_ylim(np.min(data["fitness over time"]) - 0.05,
                                    np.max(data["fitness over time"]) + 0.05)
    axes["avalanche durations"].set_ylim(
        0, np.max(np.histogram(data["avalanche durations"], HIST_BINS)[0]) + 1
    )


def add_sliders(root, frame):
    """
    Add sliders for model customisation

    Args:
        root(tk.Tk): The main application window.
        frame(tk.Frame): The frame to add the sliders to.

    Returns:
        None.

    """
    tk.Label(frame, text="Customisation", font="Verdana 12 bold").grid(
        row=0, column=0, sticky=tk.W
    )
    tk.Label(frame, text="Size: ", font="Verdana 11").grid(
        row=1, column=0, sticky=tk.W
    )
    tk.Scale(frame, from_=16, to=2048, length=200, orient=tk.HORIZONTAL,
             command=root.change_size).grid(row=1, column=1)

    tk.Label(frame, text="Interaction mode: ", font="Verdana 11").grid(
        row=2,column=0, sticky=tk.W
    )
    tk.Scale(frame, from_=1, to=2, length=200, orient=tk.HORIZONTAL,
             command=root.set_updatemode).grid(row=2, column=1)

    interaction_explaination = "\n".join((
        "1 - kill nearest neighbours",
        "2 - kill random species"
    ))
    tk.Label(frame, text=interaction_explaination, font="Verdana 9",
             anchor=tk.NW).grid(row=3,column=1, sticky=tk.W)


def add_controls(root, frame):
    """
    Add controls for the simulation.

    Args:
        root(tk.Frame): The main application window.
        frame(tk.Frame): The frame to add the controls to.

    Returns:
        tk.Button: The button to toggle visualisation of the model.

    """
    tk.Label(frame, text="Silent: ", font="Verdana 11").grid(row=4,column=0,
            sticky=tk.W)
    silentButton = tk.Button(master=frame, text="False", command=root.set_silent)
    silentButton.grid(row=5, column=1)
    tk.Label(frame, text="Simulation", font="Verdana 12 bold").grid(
        row=6,column=0, sticky=tk.W
    )
    tk.Button(master=frame, text="Start", command=root.start_simulation).grid(
        row=7, column=0
    )
    tk.Button(master=frame, text="Pause", command=root.stop_simulation).grid(
        row=7, column=1
    )
    tk.Button(master=frame, text="Restart",
              command=root.restart_simulation).grid(row=7, column=2)
    tk.Button(master=frame, text="Export", command=root.export_data).grid(
        row=8, column=0
    )
    tk.Button(master=frame, text="Quit", command=root.exit).grid(
        row=9, column=3
    )

    return silentButton
