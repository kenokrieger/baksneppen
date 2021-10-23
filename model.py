from os.path import exists
from glob import glob

import tkinter as tk
from _tkinter import TclError

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

DEFAULT_WINDOW_TITLE = "Model window"


class Model(tk.Tk):
    """Base class for physical model simulations"""

    def __init__(self, window_title=None, quit_row=19, quit_col=1):
        """
        Initialise a new model class.

        Args:
            window_title(str or None): The title of the tkinter window. Defaults
                to None meaning the default window title will be used.
            quit_row(int): The row to place the quit button.
            quit_col(int): The column to place the quit button.

        """
        super().__init__()
        for potential_icon in glob("*.ico"):
            try:
                self.iconbitmap(potential_icon)
                break
            except TclError:
                continue

        self.title(window_title if window_title is not None else DEFAULT_WINDOW_TITLE)
        self.figure = Figure(figsize=(10, 6), dpi=100)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=0, column=0, rowspan=20)

        toolbarFrame = tk.Frame(master=self)
        toolbarFrame.grid(row=21, column=0, sticky="ew")
        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbarFrame)
        self.toolbar.update()
        self.place_quit_button(quit_row, quit_col)

    def place_quit_button(self, row=19, column=1):
        """Allows to customise where to place the quit button."""
        tk.Button(master=self, text="Quit", command=self.stop).grid(row=row, column=column)

    def stop(self):
        """Close the window"""
        self.quit()
        self.destroy()
