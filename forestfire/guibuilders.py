"""
Module containing functions for building the graphical user interface for
an interactive simulation of the Bak-Sneppen model of evolution.
"""
import tkinter as tk


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
    tk.Scale(frame, from_=8, to=128, length=200, orient=tk.HORIZONTAL,
             command=root.change_size).grid(row=1, column=1)

    tk.Label(frame, text="Lightning probability: ", font="Verdana 11").grid(
        row=3,column=0, sticky=tk.W
    )
    tk.Scale(frame, from_=0, to=100, length=200, orient=tk.HORIZONTAL,
             command=root.set_lightning_probability).grid(row=3, column=1)

    tk.Label(frame, text="Tree growth: ", font="Verdana 11").grid(
        row=4,column=0, sticky=tk.W
    )
    tk.Scale(frame, from_=0, to=100, length=200, orient=tk.HORIZONTAL,
             command=root.set_tree_growth).grid(row=4, column=1)

def add_controls(root, frame):
    """
    Add controls for the simulation.

    Args:
        root(tk.Frame): The main application window.
        frame(tk.Frame): The frame to add the controls to.

    Returns:
        tuple: A button to toggle visualisation of the model and the reference
            to an info text displaying the current time of the simulation.

    """
    tk.Label(frame, text="Silent: ", font="Verdana 11").grid(row=5,column=0,
            sticky=tk.W)
    silentButton = tk.Button(master=frame, text="False", command=root.set_silent)
    silentButton.grid(row=5, column=1)
    timeInfo = tk.StringVar()
    tk.Label(frame, textvariable=timeInfo, font="Verdana 11").grid(row=6, column=2)
    timeInfo.set("t=0")
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

    tk.Button(master=frame, text="Quit", command=root.exit).grid(
        row=9, column=3
    )

    return silentButton, timeInfo
