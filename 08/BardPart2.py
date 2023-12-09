from collections import defaultdict

def parse_input(filename):
    """Parses the input file and returns the instructions and network information."""
    instructions = None
    network = {}
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if instructions is None:
                instructions = line.split()  # Convert instructions to a list
            else:
                node, connections = line.split(" = ")
                left, right = connections.split(", ")
                network[node] = {
                    "left": left,
                    "right": right,
                }
    return instructions, network

def find_start_nodes(network):
    """Finds all nodes that end with A."""
    start_nodes = []
    for node in network.keys():
        if node[-1] == "A":
            start_nodes.append(node)
    return start_nodes

def navigate(network, start_nodes, instructions):
    """
    Simultaneously navigates from all starting nodes based on the given instructions.

    Returns the number of steps taken to reach nodes ending in Z.
    """
    current_nodes = start_nodes
    step_count = 0

    while True:
        next_nodes = []
        for node in current_nodes:
            if node[-1] == "Z":
                continue
            if not instructions:
                # Reset instructions to their original order
                instructions = list(instructions)
            direction = instructions.pop(0)
            if direction == "L":
                next_node = network[node]["left"]
            else:
                next_node = network[node]["right"]
            next_nodes.append(next_node)

        if len(next_nodes) == len(start_nodes) and all(node[-1] == "Z" for node in next_nodes):
            return step_count

        current_nodes = next_nodes
        step_count += 1

def main():
    filename = r"C:\Users\etreq\Advent of Code\2023\08\inputTest.txt"
    instructions, network = parse_input(filename)
    start_nodes = find_start_nodes(network)

    steps = navigate(network, start_nodes, instructions)
    print(f"Number of steps to reach nodes ending in Z: {steps}")

if __name__ == "__main__":
    main()
