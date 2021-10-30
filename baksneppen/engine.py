from numpy import savetxt

from baksneppen.constructors import (add_subplots, add_controls, add_sliders,
                                     add_artists, update_artists, update_axes)
from baksneppen.destructors import clear
from baksneppen.model import BakSneppenModel

from simulations.engine import SimulationEngine


class BakSneppenEngine(SimulationEngine):
    """The main application for the Bak Sneppen model simulation. """

    def __init__(self):
        """Initialise the simulation window"""
        super().__init__("Bak-Sneppen evolution model")
        self.axes = add_subplots(self.figure)
        self.lines, self.bars = add_artists(self.axes)
        self.model = BakSneppenModel()

        add_sliders(self, self.controlPanel)
        self.silentButton = add_controls(self, self.controlPanel)

        self.silent = False
        self.running = False

    def clear_figure(self):
        """Clear all lines and bars from the figure but keep labels intact. """
        clear(self.lines, self.bars)

    def start_simulation(self):
        """Start the simulation. """
        if self.running:
            return
        self.running = True
        self.simulate()

    def restart_simulation(self):
        """Restart the simulation. """
        self.running = False
        self.clear_figure()
        self.model.set_up_simulation()
        self.running = True
        self.simulate()

    def stop_simulation(self):
        """Stop the simulation. """
        self.running = False

    def simulate(self):
        """Advance the simulation. """
        if self.running:
            self.model.update()
            if not self.silent:
                self.visualise()
            self.after(1, self.simulate)

    def set_silent(self):
        """Toggles the visualisation of the simulation. """
        self.silent = not self.silent
        self.silentButton["text"] = ("True" if self.silent else "False")

    def change_size(self, size):
        """Change the size of the simulation. """
        self.model.set_size(size)

    def set_updatemode(self, updatemode):
        """
        Change the algorithm used for the update.

        Args:
            updatemode(int): Specify which algorithm to use.
                1 - kill nearest neighbours
                2 - kill random species
        """
        self.model.set_updatemode(updatemode)

    def export_data(self):
        """Export the measured data aswell as a snapshot of the current figure. """
        data = self.model.get_data()
        savetxt("fitness.dat", data["fitness over time"])
        savetxt("avalanche_durations.dat", data["avalanche durations"])
        self.figure.savefig("snapshot_{}.png".format(data["time"]))

    def visualise(self):
        """Visualise the data of the model. """
        data = self.model.get_data()
        update_artists((self.lines, self.bars), data)
        update_axes(self.axes, data)
        self.canvas.draw()
        return
