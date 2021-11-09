"""Contains routines to determine a cells state"""

SOIL = 0
FIRE = -1
TREE = 1


def is_burning(cell):
    return cell == FIRE


def is_soil(cell):
    return cell == SOIL


def is_tree(cell):
    return cell == TREE


def neighbours_are_burning(trees, row, col):
    """
    """
    neighbours = [
        trees[row - 1, col], # upper neighbour
        trees[row + 1 if row + 1 < trees.shape[0] else 0, col], # lower neighbour
        trees[row, col - 1], # left neighbour
        trees[row, col + 1 if col + 1 < trees.shape[1] else 0] # right neighbour
    ]

    return True if any(is_burning(n) for n in neighbours) else False
