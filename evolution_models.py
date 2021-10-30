from time import sleep

import numpy as np
from random import random, randint

import tkinter as tk

import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker

from model import Model

HIST_BINS = np.arange(0, 7, 1)


class BakSneppen(Model):
    """The evolution model of Bak and Sneppen"""

    def __init__(self):
        """Initialise the root window for the model"""
        super().__init__("Bak Sneppen Evolution model", 20, 3)
        tk.Label(self, text="Customisation", font="Verdana 12 bold").grid(row=0,column=1, sticky=tk.W)
        self.size = 16
        self.silent = False
        self.change = []
        self.avalanche_duration = 1
        self.avalanche_durations = []
        self._add_sliders()
        self._add_controls()
        self.generate_subplots()
        self.set_up_simulation()
        self.running = False


    def _add_sliders(self):
        """Add sliders for model customisation"""
        tk.Label(self, text="Size: ", font="Verdana 11").grid(row=2,column=1, sticky=tk.W)
        size_slider = tk.Scale(self, from_=16, to=2048, length=200, orient=tk.HORIZONTAL, command=self.change_size)
        size_slider.grid(row=2, column=2)

        tk.Label(self, text="Interaction mode: ", font="Verdana 11").grid(row=3,column=1, sticky=tk.W)
        interaction_slider = tk.Scale(self, from_=1, to=2, length=200, orient=tk.HORIZONTAL, command=self.set_updatemode)
        interaction_slider.grid(row=3, column=2)

        interaction_explaination = "\n".join((
            "1 - kill nearest neighbours",
            "2 - kill random species"
        ))
        tk.Label(self, text=interaction_explaination, font="Verdana 9", anchor=tk.NW).grid(row=4,column=2, sticky=tk.W)

    def _add_controls(self):
        """Add controls for the simulation"""
        tk.Label(self, text="Silent: ", font="Verdana 11").grid(row=5,column=1, sticky=tk.W)
        self.silentButton = tk.Button(master=self, text="False", command=self.set_silent)
        self.silentButton.grid(row=5, column=2)
        tk.Label(self, text="Simulation", font="Verdana 12 bold").grid(row=6,column=1, sticky=tk.W)
        tk.Button(master=self, text="Start", command=self.start_simulation).grid(row=7, column=1)
        tk.Button(master=self, text="Pause", command=self.stop_simulation).grid(row=7, column=2)
        tk.Button(master=self, text="Restart", command=self.restart_simulation).grid(row=7, column=3)
        tk.Button(master=self, text="Export", command=self.export).grid(row=8, column=1)

    def restart_simulation(self):
        """Restart the simulation"""
        self.running = False
        sleep(0.3)
        self.set_up_simulation()
        self.running = True
        self.animate()

    def start_simulation(self):
        """Start the simulation"""
        if self.running:
            return
        self.running = True
        self.animate()

    def stop_simulation(self):
        """Stop the simulation"""
        self.running = False

    def animate(self):
        """Display the animation"""
        if self.running:
            self.update()
            self.after(1, self.animate)

    def set_silent(self):
        """Changes whether to visualise the simulation or not"""
        self.silent = not self.silent
        self.silentButton["text"] = ("True" if self.silent else "False")

    def export(self):
        """Export data"""
        self.running = False
        sleep(0.2)
        np.savetxt("fitness_change.dat", self.change)
        np.savetxt("avalanche_durations.dat", self.avalanche_durations)
        self.figure.savefig("plot.png", dpi=300)

    def set_up_simulation(self):
        """Create the arrays needed for the simulation"""
        self.scatterplot.set_data([], [])
        self.least_fitness_line.set_data([], [])
        self.avalancheline.set_data([], [])
        self.duration_line.set_data([], [])
        for rect in self.duration_histogram.patches:
            rect.set_height(0.01)

        self.species = np.random.rand(self.size)
        self.avalanche_duration = 1
        self.avalanche_durations = []
        self.least_fitness = 0.0
        self.updatemode = 1
        self.time = 1
        self.scatterplot.set_data(np.arange(0, self.species.shape[0], 1), self.species)
        self.liveview.set_xlim(-1, self.species.shape[0])
        self.liveview.set_ylim(0, 1)
        self.least_fitness_line.set_data([-1, self.size], self.least_fitness)
        self.canvas.draw()

    def update(self):
        """The update algorithm for the Bak-Sneppen model."""
        weakling_index = np.argmin(self.species)
        least_fitness = self.species[weakling_index]

        if least_fitness > self.least_fitness:
            self.change.append(least_fitness - self.least_fitness)
            self.least_fitness = least_fitness
            self.avalanche_durations.append(np.log10(self.avalanche_duration))
            self.avalanche_duration = 1
        else:
            self.avalanche_duration += 1
            self.change.append(0.0)

        if self.updatemode == 1:
            left_neighbour = weakling_index - 1
            right_neighbour = (weakling_index + 1) % self.size

            for idx in (weakling_index, left_neighbour, right_neighbour):
                self.species[idx] = random()
        else:
            self.species[weakling_index] = random()
            self.species[randint(0, self.species.shape[0] - 1)] = random()

        if not self.silent:
            self.visualise()
        self.time += 1

    def change_size(self, size):
        """
        Expand or trunctuate the species array in one dimension.

        Args:
            size(int): The new size of the array.

        """
        self.size = int(size)
        if self.size > self.species.shape[0]:
            new = np.random.rand(self.size)
            new[:self.species.shape[0]] = self.species
            self.species = new
        elif self.size < self.species.shape[0]:
            self.species = self.species[:self.size]

        self.liveview.set_xlim(0, self.size)
        self.scatterplot.set_data(np.arange(0, self.species.shape[0], 1), self.species)
        self.least_fitness_line.set_xdata([-1, self.size])
        self.canvas.draw()

    def set_updatemode(self, updatemode):
        """
        Change the algorithm used for the update.

        Args:
            updatemode(int): Specify which algorithm to use.
                1 - kill nearest neighbours
                2 - kill random species
        """
        self.updatemode = updatemode

    def generate_subplots(self):
        """Add two subplots to the figure"""
        grid = gridspec.GridSpec(ncols=2, nrows=2, figure=self.figure)
        self.liveview = self.figure.add_subplot(grid[0:, 0])
        self.liveview.set_title("Fitness of the species")
        self.liveview.set_xlabel("Position in array")
        self.liveview.set_ylabel("Fitness")
        self.scatterplot, = self.liveview.plot([], [], color="blue", marker="o", linewidth=0)
        self.least_fitness_line, = self.liveview.plot([], [], color="blue", linestyle="dashed")

        self.avalanches = self.figure.add_subplot(grid[0, 1])
        self.avalanches.set_title("Change in minimum fitness")
        self.avalanches.set_xlabel("time")
        self.avalanches.set_ylabel("Change in minimum fitness")
        self.avalancheline, = self.avalanches.plot([0,1], [1,1], color="blue")

        self.durations = self.figure.add_subplot(grid[1, 1])
        self.durations.set_title("Histogram of avalanche durations")
        self.durations.set_xlabel("Duration")
        self.durations.xaxis.set_major_formatter(ticker.FormatStrFormatter("$10^%d$"))
        self.durations.set_ylabel("Frequency")
        _, _, self.duration_histogram = self.durations.hist([0.01], HIST_BINS, rwidth=0.9)
        self.duration_line, = self.durations.plot([], [], color="blue")
        self.figure.tight_layout()
        self.canvas.draw()

    def visualise(self):
        """Visualise the model"""
        self.scatterplot.set_ydata(self.species)
        self.least_fitness_line.set_ydata(self.least_fitness)
        self.avalancheline.set_data(np.arange(0, len(self.change), 1), np.array(self.change))
        self.avalanches.set_xlim(-0.5, self.time + 1)
        self.avalanches.set_ylim(-0.001, np.max(self.change) + 0.01)

        n, _ = np.histogram(self.avalanche_durations, HIST_BINS)
        for count, rect in zip(n, self.duration_histogram.patches):
            rect.set_height(count)

        self.durations.set_ylim(0.1, np.max(n) + 2)
        self.durations.set_yscale("log")
        self.canvas.draw()
