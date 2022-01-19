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
        "and supply the system size (-s) and the " \
        "number of updates (-u) as command line arguments. If no number of " \
        "updates is supplied the script will run until it is faces a Keyboard " \
        "interrupt (Ctrl + C)\n",
        "Example: forestfire_main.py nogui -f=0.0001 -t=0.007"
    ))
    TKINTER_INSTALLED = False


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
        print("Could not convert input '{}' to {}".format(string_value,
                                                          conversion_type))

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
    size = None
    nupdates = None
    tree_probability = None
    fire_probability = None
    # the first command line argument is always the name of the script.
    command_line_args = argv[1:]

    for arg in command_line_args:
        if "nogui" in arg:
            use_gui = False
        elif "-s" in arg:
            size = _convert(arg.split("=")[1], int)
        elif "-u" in arg:
            nupdates = _convert(arg.split("=")[1], int)
        elif "-t" in arg:
            tree_probability = _convert(arg.split("=")[1], float)
        elif "-f" in arg:
            fire_probability = _convert(arg.split("=")[1], float)
    return use_gui, size, nupdates, tree_probability, fire_probability


def nogui_simulation(size, lightning_probability, tree_growth, nupdates):
    """
    Simulation without the graphical user interface.

    Args:
        size(int): The system size for the simulation.

    Returns:
        None.

    """
    model = ForestFireModel(size, lightning_probability, tree_growth)

    if nupdates is not None:
        for update in range(nupdates):
            model.update()
            if not (model.time % 1000):
                print(f"completed {model.time}/{nupdates} iterations.")
    else:
        while True:
            try:
                model.update()
                if not (model.time % 1000):
                    print(f"completed {model.time} iterations.")
            except KeyboardInterrupt:
                break

    data = model.get_data()
    meta_info = "\n".join((
        f"t = {data['time']}",
        f"n = {data['system size']}",
        f"t = {data['tree growth']}",
        f"f = {data['lightning']}"
    ))
    print("Stopping simulation and saving data...")
    savetxt("avalanche_sizes.dat", data["avalanche sizes"], header=meta_info)
    savetxt("avalanche_durations.dat", data["avalanche durations"],
            header=meta_info + ", values as log10(duration)")


def main():
    """Main function of the script. """
    use_gui, size, nupdates, tree_probability, fire_probability = parse_command_line_args()

    if use_gui and not TKINTER_INSTALLED:
        print(ERRMSG)
        return

    if use_gui:
        if any([p is not None for p in (nupdates, size, tree_probability, fire_probability)]):
            print("Warning: Some command line parameters are ignored.")

        engine = ForestFireEngine()
        engine.mainloop()
    else:
        nogui_simulation(size, fire_probability, tree_probability, nupdates)


if __name__ == "__main__":
    main()
