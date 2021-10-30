"""
Contains a class for simulating the Bak-Sneppen model of evolution.
"""
import numpy as np

from random import random, randint

DEFAULT_SIZE = 16


class BakSneppenModel:
    """The evolution model of Bak and Sneppen"""

    def __init__(self, size=None):
        """Initialise the model"""
        self.size = size if size is not None else DEFAULT_SIZE
        self.set_up_simulation()

    def clear(self):
        """Restart the simulation"""
        self.set_up_simulation()

    def set_up_simulation(self):
        """Initialise all values needed for the simulation"""
        self.species = np.random.rand(self.size)
        self.avalanche_duration = 1
        self.avalanche_durations = []
        self.least_fitness = 0.0
        self.fitness_over_time = []
        # update mode can be 1 or 2
        self.updatemode = 1
        self.time = 0

    def update(self):
        """The update algorithm for the Bak-Sneppen model."""
        weakling_index = np.argmin(self.species)
        least_fitness = self.species[weakling_index]

        if least_fitness > self.least_fitness:
            self.least_fitness = least_fitness
            self.avalanche_durations.append(np.log10(self.avalanche_duration))
            self.avalanche_duration = 1
        else:
            self.avalanche_duration += 1

        if self.updatemode == 1:
            left_neighbour = weakling_index - 1
            right_neighbour = (weakling_index + 1) % self.size

            for idx in (weakling_index, left_neighbour, right_neighbour):
                self.species[idx] = random()
        else:
            self.species[weakling_index] = random()
            self.species[randint(0, self.species.shape[0] - 1)] = random()

        self.fitness_over_time.append(self.least_fitness)
        self.time += 1

    def set_size(self, size):
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

    def set_updatemode(self, updatemode):
        """
        Change the algorithm used for the update.

        Args:
            updatemode(int): Specify which algorithm to use.
                1 - kill nearest neighbours
                2 - kill random species
        """
        self.updatemode = updatemode

    def get_data(self):
        """Get the measured data and meta data. """
        return {
            "time": self.time,
            "system size": self.size,
            "species": self.species,
            "fitness over time": np.array(self.fitness_over_time),
            "avalanche durations": np.array(self.avalanche_durations)
        }
