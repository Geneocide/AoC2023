# I didn't initially see how this could be made efficient. And then I initially did a simple multiplication of all answers instead of LCM.
# I Thought about trying to parallelize the code, I'm glad I didn't

from math import lcm
from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

rightLeftPattern = None
nodeConnections = {}
startNodes = []


def followSteps():
    direction = rightLeftPattern[stepCount % len(rightLeftPattern)]
    return nodeConnections[currentNode][int(direction)]


# def followSteps():
#     newCurrentNodes = []
#     for node in currentNodes:
#         direction = rightLeftPattern[stepCount % len(rightLeftPattern)]
#         newNode = nodeConnections[node][int(direction)]
#         newCurrentNodes.append(newNode)
#     return newCurrentNodes


with open(filepath, "r") as file:
    for line in file:
        line = line.strip()
        if len(line) == 0:  # get rid of spacer line in input
            continue
        if "=" in line:  # normal instruction
            node, connections = line.split(" = ")
            if node[-1] == "A":
                startNodes.append(node)  # now starting at all nodes that end in A
            left, right = connections.replace("(", "", 1).replace(")", "", 1).split(",")
            nodeConnections[node] = (left.strip(), right.strip())
        else:  # initial RL pattern
            rightLeftPattern = line.replace("L", "0").replace("R", "1")

stepCounts = []
for currentNode in startNodes:
    stepCount = 0
    while currentNode[-1] != "Z":
        currentNode = followSteps()
        stepCount += 1
    stepCounts.append(stepCount)

print(stepCounts)
print(
    "Steps until all __Z: " + str(lcm(*stepCounts))
)  # answer 17193155135366481952862161 (high), 13663968099527
