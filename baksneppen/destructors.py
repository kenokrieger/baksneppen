

def clear(lines, bars):
    """
    Reset the lines and bars in the plot to contain no data points.

    Args:
        lines(dict): All the lines to clear.
        bars(dict): All the bars to clear.

    Returns:
        None.

    """
    for line in lines:
        lines[line].set_data([], [])

    for bar in bars:
        for rect in bars[bar]:
            rect.set_height(0)
