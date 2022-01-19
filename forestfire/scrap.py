forest = np.ones((10, 10))
avalanches = np.zeros(forest.shape)
old_avalanches = avalanches.copy()


for row in range(forest.shape[0]):
    for col in range(forest.shape[1]):

        cell = forest[row, col]

        ...

        if cell_state.is_fire(updated_cell):

            add_to_avalanche(row, col)


def add_to_avalanche(avalanches, row, col):
    neighbours = [
        avalanches[row - 1, col] if row - 1 > 0 else 0, # upper neighbour
        avalanches[row + 1, col] if row + 1 < trees.shape[0] else 0, # lower neighbour
        avalanches[row, col - 1] if col - 1 > 0 else 0, # left neighbour
        avalanches[row, col + 1]  if col + 1 < trees.shape[1] else 0 # right neighbour
    ]

    avalanche_number = np.max(neighbours)

    if avalanche_number == 0:
        avalanche_number = np.max(avalanches) + 1

    else:
        for neighbour in neighbours:
            if neighbour and neighbour != avalanche_number:
                avalanches[np.where(avalanche) == neighbour] = avalanche_number


def check_avalanches(avalanches, old_avalanches):

    
