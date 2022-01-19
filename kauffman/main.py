import numpy as np

N = 20
K = 2


class BooleanNetwork:
    def __init__(self, number_of_nodes, number_of_connections):
        self.nodes = np.random.randint(0, 2, (number_of_nodes, ))
        # array storing the indices of k edges for each node
        self.connections = np.random.randint(
            0, number_of_nodes, (number_of_nodes, number_of_connections)
        )
        # array storing the indices of the boolean functions for each possible
        # node combination
        self.function_choices = np.random.randint(
            0, 2, (number_of_nodes, number_of_connections, number_of_connections)
        )
        self.boolean_functions = np.empty((2, number_of_connections, number_of_connections), dtype=int)
        self.boolean_functions[0, :] = np.zeros((number_of_connections, number_of_connections))
        self.boolean_functions[1, :] = np.ones((number_of_connections, number_of_connections))
        self.time = 0

    def _update_once(self):
        new_state = np.empty(self.nodes.shape, dtype=int)
        for node_position in range(self.nodes.shape[0]):
            ingoing_nodes = self.connections[node_position]
            #new_state[node_position] = self.boolean_functions[self.function_choices[*ingoing_nodes], *ingoing_nodes]

        self.nodes = new_state
        self.time += 1

    def update(self, timesteps=1):
        for timestep in range(timesteps):
            self._update_once()

    def print_state(self):
        print(f"t = {self.time}: {self.nodes}")
    def __str__(self):
        return (
f"""
Random Boolean Network:
with nodes
{self.nodes}
and connections
{self.connections}
and boolean functions for each node
{self.function_choices}
""")



if __name__ == "__main__":
    new_network = BooleanNetwork(N, K)
    print(new_network)
    for i in range(10):
        new_network.update()

    new_network.print_state()
