from pathlib import Path
import networkx as nx

filepath = Path(__file__).parent / "input.txt"
network = {}


with open(filepath, "r") as file:
    for line in file:
        line = line.strip()
        namedNode, otherNodes = line.split(": ")
        otherNodes = otherNodes.split()
        network[namedNode] = otherNodes

network = nx.Graph(network)

network.remove_edges_from(nx.minimum_edge_cut(network))
cc = list(nx.connected_components(network))

print(
    f"What do you get if you multiply the sizes of these two groups together? Answer: {len(cc[0]) * len(cc[1])}"
)  # answer 495607
