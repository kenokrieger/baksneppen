from sys import argv

from numpy import savetxt

from forestfire.model import ForestFireModel

try:
    from forestfire.engine import ForestFireEngine
    TKINTER_INSTALLED = True
except ImportError as err:
    ERRMSG = "\n".join((
        "Import Error: {}\n".format(err),
        "Install python-tkinter if you want to use the graphical user interface.",
        "(sudo apt-get install python3-tk).",
        "You may also run the script over the command line by adding 'nogui' " \
        "and supply the system size (-s), the update algorithm (-m) and the " \
        "number of updates (-u) as command line arguments. If no number of " \
        "updates is supplied the script will run until it is faces a Keyboard " \
        "interrupt (Ctrl + C)\n",
        "Example: main.py nogui -s=1000 -u=10000"
    ))
    TKINTER_INSTALLED = False

DEFAULT_SYSTEM_SIZE = 8


def _convert(string_value, conversion_type):
    """
    Convert a string value into the desired type.

    Args:
        string_value(string): The value to convert.
        conversion_type(type): The type to cast to.

    Returns:
        type: The casted value.

    """
    try:
        converted_value = conversion_type(string_value)
    except ValueError as err:
        print("Could not convert input '{}' to integer".format(string_value))

    return converted_value


def parse_command_line_args():
    """
    Minimal command line parser to translate user input instructions for the
    programm.

    Args:
        None.

    Returns:
        tuple: The parsed values found in the command line input.

    """
    use_gui = True
    size = DEFAULT_SYSTEM_SIZE
    nupdates = None
    mode = 1
    # the first command line argument is always the name of the script.
    command_line_args = argv[1:]

    for arg in command_line_args:
        if "nogui" in arg:
            use_gui = False
        elif "-s" in arg:
            size = _convert(arg.split("=")[1], int)
        elif "-u" in arg:
            nupdates = _convert(arg.split("=")[1], int)
        elif "-m" in arg:
            mode = _convert(arg.split("=")[1], int)
    return use_gui, size, mode, nupdates


def nogui_simulation(size, updatemode, nupdates):
    """
    Simulation without the graphical user interface.

    Args:
        size(int): The system size for the simulation.
        updatemode(int): The algorithm to use for the updates.
            1 - kill nearest neighbours
            2 - kill one random neighbour
        nupdates(int): The number of updates to perform. If nupdates is None
            an infinite while loop will be started until interrupted.

    Returns:
        None.

    """
    model = BakSneppenModel()
    model.set_size(size)
    model.set_updatemode(updatemode)

    if nupdates is not None:
        for update in range(nupdates):
            model.update()
            if not (model.time % 1000):
                print(f"completed {model.time}/{nupdates} iterations.")
                print(f"l = {model.least_fitness}")
    else:
        while True:
            try:
                model.update()
            except KeyboardInterrupt:
                break

            if not (model.time % 1000):
                print(f"completed {model.time} iterations.")
                print(f"l = {model.least_fitness}")

    data = model.get_data()
    meta_info = ", ".join((
        f"t = {data['time']}", f"n = {data['system size']}"
    ))
    print("Stopping simulation and saving data...")
    savetxt("fitness.dat", data["fitness over time"], header=meta_info)
    savetxt("avalanche_durations.dat", data["avalanche durations"],
            header=meta_info + ", values as log10(duration)")


def main():
    """Main function of the script. """
    use_gui, size, mode, nupdates = parse_command_line_args()

    if use_gui and not TKINTER_INSTALLED:
        print(ERRMSG)
        return

    if use_gui:
        if any([p is not None for p in (nupdates, )]):
            print("Warning: Some command line parameters are ignored.")

        engine = ForestFireEngine()
        engine.change_size(size)
        engine.mainloop()
    else:
        nogui_simulation(size, mode, nupdates)


if __name__ == "__main__":
    main()
