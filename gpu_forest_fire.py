SIZE = 128
LIGHTNING_PROBABILITY = 1e-4
TREE_GROWTH = 7e-3
NUPDATES = 1_000_000


@cuda.jit
def copy(source, destination):
    destination[*cuda.grid(2)] = source[*cuda.grid(2)]


@cuda.jit
def update_trees(is_black, rng_states, source, checkerboard_agents,
                 lightning_probability, tree_growth, shape):
    """
    Update all spins in one array according to the Forest Fire Model.
    """
    startx, starty = cuda.grid(2)
    stridex, stridey = cuda.gridsize(2)
    # Linearised thread index
    thread_id = (starty * stridex) + startx

    # Use strided loops over the array
    for row in range(starty, shape[0], stridey):
        for col in range(startx, shape[1], stridex):
            row = cuda.blockIdx.x * cuda.blockDim.x + cuda.threadIdx.x
            col = cuda.blockIdx.y * cuda.blockDim.y + cuda.threadIdx.y
            cell = source[row, col]

            if cell == -1:
                # cell becomes soil
                source[row, col] = 0
                return

            random = xoroshiro128p_uniform_float32(rng_states, thread_id)

            if cell == 0:
                if random < tree_growth:
                    # cell becomes tree
                    source[row, col] = 1
                return

            # last case: cell is a tree
            lower_neighbor_row = row + 1 if (row + 1 < shape[0]) else None
            upper_neighbor_row = row - 1 if row - 1 > 0 else None
            right_neighbor_col = col + 1 if (col + 1 < shape[1]) else None
            left_neighbor_col = col - 1 if col -1 > 0 else None

            if is_black:
                horizontal_neighbor_col = left_neighbor_col if row % 2 else right_neighbor_col
            else:
                horizontal_neighbor_col = right_neighbor_col if row % 2 else left_neighbor_col

            for neighbour_row in (row, lower_neighbor_row, upper_neighbor_row):
                if row is not None and checkerboard_agents[row, col] == -1:
                    source[row, col] = -1
                    return

            if horizontal_neighbor_col is not None and checkerboard_agents[row, horizontal_neighbor_col] == -1:
                source[row, col] = -1
                return


def update(rng_states, d_buffer, black, white, lightning_probability,
           tree_growth, shape):
    """
    Update both arrays.
    """
    threads_per_block = (8, 8)
    blocks = (8, 8)

    update_trees[blocks, threads_per_block](True, rng_states, black, white,
                                            lightning_probability, tree_growth,
                                            shape)
    cuda.synchronize()
    update_trees[blocks, threads_per_block](False, rng_states, white, black,
                                            lightning_probability, tree_growth,
                                            shape)


if __name__ == "__main__":
    shape = (SIZE, SIZE // 2)
    lightning_probability = LIGHTNING_PROBABILITY
    tree_growth = TREE_GROWTH

    black_trees = np.zeros(shape, dtype=np.int32)
    d_black_trees = cuda.to_device(black_trees)
    white_trees = np.zeros(shape, dtype=np.int32)
    d_white_trees = cuda.to_device(white_trees)
    buffer = np.zeros(shape, dtype=np.int32)
    d_buffer = cuda.to_device(buffer)

    threads_per_block = (16, 16)
    blocks = (16, 16)
    total_number_of_threads = 16 ** 4
    rng_states = create_xoroshiro128p_states(total_number_of_threads, seed=seed)

    for iteration in range(NUPDATES):
        update(rng_states, d_buffer, d_black_trees, d_white_trees,
               lightning_probability, tree_growth, shape)

    cuda.close()
