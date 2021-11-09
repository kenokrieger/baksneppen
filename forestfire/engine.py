"""
Contains the root window for an interactive simulation of the Bak-Sneppen
model of evolution.
"""
from numpy import savetxt

from simulations.engine import SimulationEngine

from forestfire.plothelpers import add_subplots, add_artists, update_artists, update_axes, clear
from forestfire.guibuilders import add_controls, add_sliders

from forestfire.model import ForestFireModel


class ForestFireEngine(SimulationEngine):
    """The main application for the Bak Sneppen model simulation. """

    def __init__(self):
        """Initialise the simulation window"""
        super().__init__("Forest Fire Model")
        self.axes = add_subplots(self.figure)
        self.lines, self.bars = add_artists(self.axes)
        self.model = ForestFireModel()

        add_sliders(self, self.controlPanel)
        self.silentButton, self.timeText = add_controls(self, self.controlPanel)

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
        self.model.clear()
        self.running = True
        self.simulate()

    def stop_simulation(self):
        """Stop the simulation. """
        self.running = False

    def simulate(self):
        """Advance the simulation. """
        if self.running:
            self.model.update()
            self.timeText.set(f"t = {self.model.time}")
            if not self.silent:
                self.visualise()
            self.after(1, self.simulate)

    def set_silent(self):
        """Toggles the visualisation of the simulation. """
        self.silent = not self.silent
        self.silentButton["text"] = "True" if self.silent else "False"

    def change_size(self, size):
        """Change the size of the simulation. """
        self.model.set_size(size)

    def set_scaling(self, scaling):
        self.model.set_scaling(int(scaling))

    def set_lightning_probability(self, lightning_probability):
        self.model.set_lightning_probability(int(lightning_probability) / 100_000)

    def set_tree_growth(self, tree_growth):
        self.model.set_tree_growth(int(tree_growth) / 100_000)

    def export_data(self):
        """Export the measured data as well as a snapshot of the current figure. """
        data = self.model.get_data()
        meta_info = ", ".join((
            f"t = {data['time']}", f"n = {data['system size']}"
        ))
        self.figure.savefig("snapshot_{}.png".format(data["time"]))

    def visualise(self):
        """Visualise the data generated by the model. """
        data = self.model.get_data()
        update_artists((self.lines, self.bars), data)
        # update_axes(self.axes, data)
        self.canvas.draw()
