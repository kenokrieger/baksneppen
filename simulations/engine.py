import tkinter as tk

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

DEFAULT_WINDOW_TITLE = "Simulation"


class SimulationEngine(tk.Tk):
    """Base class for physical model simulations"""

    def __init__(self, window_title=None, icon=None):
        """
        Initialise a new model class.

        Args:
            window_title(str or None): The title of the tkinter window. Defaults
                to None meaning the default window title will be used.
            quit_row(int): The row to place the quit button.
            quit_col(int): The column to place the quit button.

        """
        super().__init__()

        if icon is not None:
            self.iconbitmap(icon)

        self.title(window_title if window_title is not None else DEFAULT_WINDOW_TITLE)
        self.figure = Figure(figsize=(10, 6), dpi=100)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0)

        toolbarFrame = tk.Frame(master=self)
        toolbarFrame.grid(row=1, column=0, sticky="ew")
        NavigationToolbar2Tk(self.canvas, toolbarFrame).update()

        self.controlPanel = tk.Frame(master=self)
        self.controlPanel.grid(row=0, column=1, sticky="ew")

    def get_figure(self): return self.figure

    def get_controlPanel(self): return self.controlPanel

    def update_figure(self):
        self.canvas.draw()

    def exit(self):
        """Close the window"""
        self.quit()
        self.destroy()
