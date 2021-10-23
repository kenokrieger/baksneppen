import tkinter as tk

import numpy as np
from random import random, randint

from time import sleep

from model import Model


class BakSneppen(Model):
    """The evolution model of Bak and Sneppen"""

    def __init__(self):
        """Initialise the root window for the model"""
        super().__init__("Bak Sneppen Evolution model", 20, 3)
        tk.Label(self, text="Customisation", font="Verdana 12 bold").grid(row=0,column=1, sticky=tk.W)
        self.size = 16
        self.change = []
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

    def export(self):
        self.running = False
        np.savetxt("fitness_change.dat", self.change)

    def set_up_simulation(self):
        """Create the arrays needed for the simulation"""
        self.scatterplot.set_data([], [])
        self.least_fitness_line.set_data([], [])

        while self.avalanches.lines:
            self.avalanches.lines[0].remove()

        self.species = np.random.rand(self.size)
        self.least_fitness = 0.0
        self.updatemode = 1
        self.time = 1
        self.fitness_change = [0, 0]
        self.scatterplot.set_data(np.arange(0, self.species.shape[0], 1), self.species)
        self.liveview.set_xlim(-1, self.species.shape[0])
        self.liveview.set_ylim(0, 1)
        self.least_fitness_line.set_data([-1, self.size], self.least_fitness)
        self.canvas.draw()

    def update(self):
        """The update algorithm for the Bak-Sneppen model."""
        weakling_index = np.argmin(self.species)
        least_fitness = self.species[weakling_index]
        self.fitness_change[1] = 0.0
        if least_fitness > self.least_fitness:
            self.fitness_change[1] = least_fitness - self.least_fitness
            self.least_fitness = least_fitness

        if self.updatemode == 1:
            left_neighbour = weakling_index - 1
            right_neighbour = (weakling_index + 1) % self.size

            for idx in (weakling_index, left_neighbour, right_neighbour):
                self.species[idx] = random()
        else:
            self.species[weakling_index] = random()
            self.species[randint(0, self.species.shape[0] - 1)] = random()

        self.visualise()
        self.time += 1
        self.fitness_change[0] = self.fitness_change[1]
        self.change.append(self.fitness_change[0])

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
        self.liveview = self.figure.add_subplot(121)
        self.liveview.set_title("Fitness of the species")
        self.liveview.set_xlabel("Position in array")
        self.liveview.set_ylabel("Fitness")
        self.scatterplot, = self.liveview.plot([], [], color="blue", marker="o", linewidth=0)
        self.least_fitness_line, = self.liveview.plot([], [], color="blue", linestyle="dashed")

        self.avalanches = self.figure.add_subplot(122)
        self.avalanches.set_title("Change in minimum fitness")
        self.avalanches.set_xlabel("time")
        self.avalanches.set_ylabel("Change in minimum fitness")
        self.figure.tight_layout()
        self.canvas.draw()

    def visualise(self):
        self.scatterplot.set_ydata(self.species)
        self.least_fitness_line.set_ydata(self.least_fitness)
        self.avalanches.plot([self.time - 1, self.time], self.fitness_change, color="blue")
        self.avalanches.set_xlim(self.avalanches.get_xlim()[0], self.time + 1)
        self.canvas.draw()
