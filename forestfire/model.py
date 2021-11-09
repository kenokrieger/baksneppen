"""
Contains a class for simulating the Forest Fire model.
"""
import numpy as np

from random import random, randint

from forestfire import cell_state

DEFAULT_SIZE = 8
DEFAULT_LIGHTNING_PROBABILITY = 0.001
DEFAULT_TREE_GROWTH = 0.001


class ForestFireModel:
    """The forest fire model"""

    def __init__(self, size=None, lightning_probability=None,
                 tree_growth=None):
        """Initialise the model"""
        self.size = size if size is not None else DEFAULT_SIZE
        self.lightning_probability = lightning_probability if lightning_probability is not None \
                                     else DEFAULT_LIGHTNING_PROBABILITY
        self.tree_growth = tree_growth if tree_growth is not None \
                           else DEFAULT_TREE_GROWTH

        self.scaling = 1
        self.set_up_simulation()

    def clear(self):
        """Restart the simulation"""
        self.set_up_simulation()

    def set_up_simulation(self):
        """Initialise all values needed for the simulation"""
        self.forest = np.zeros((self.size, self.size))
        self.time = 0

    def update(self):
        """The update algorithm for the Forest Fire model."""
        for col in range(self.size):
            for row in range(self.size):
                cell = self.forest[row, col]

                if cell_state.is_burning(cell):
                    self.forest[row, col] = cell_state.SOIL
                elif cell_state.is_tree(cell):
                    if cell_state.neighbours_are_burning(self.forest, row, col):
                        self.forest[row, col] = cell_state.FIRE
                    elif random() < self.scaling * self.lightning_probability:
                        self.forest[row, col] = cell_state.FIRE
                elif cell_state.is_soil(cell) and random() < self.scaling * self.tree_growth:
                    self.forest[row, col] = cell_state.TREE
        self.time += 1

    def set_scaling(self, scaling): self.scaling = scaling

    def set_tree_growth(self, tree_growth): self.tree_growth = tree_growth

    def set_lightning_probability(self, lightning_probability): self.lightning_probability = lightning_probability

    def set_size(self, size):
        """
        Expand or trunctuate the tree array.

        Args:
            size(int): The new size of the array.

        """
        self.size = int(size)
        if self.size > self.forest.shape[0]:
            new = np.zeros((self.size, self.size))
            new[:self.forest.shape[0], :self.forest.shape[1]] = self.forest
            self.forest = new
        elif self.size < self.forest.shape[0]:
            self.forest = self.forest[:self.size, :self.size]



    def get_data(self):
        """Get the measured data and meta data. """
        return {
            "time": self.time,
            "system size": self.size,
            "forest": self.forest
        }
