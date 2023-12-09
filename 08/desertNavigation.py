from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

rightLeftPattern = None
nodeConnections = {}


def followSteps():
    direction = rightLeftPattern[stepCount % len(rightLeftPattern)]
    return nodeConnections[currentNode][int(direction)]


with open(filepath, "r") as file:
    for line in file:
        line = line.strip()
        if len(line) == 0: #get rid of spacer line in input
            continue
        if "=" in line:  # normal instruction
            node, connections = line.split(" = ")
            left, right = connections.replace("(", "", 1).replace(")", "", 1).split(",") #Bard did [1:-1] to get rid of (), which would have been better
            nodeConnections[node] = (left.strip(), right.strip())
        else:  # initial RL pattern
            rightLeftPattern = line.replace("L", "0").replace("R", "1")

currentNode = "AAA"
stepCount = 0
while currentNode != "ZZZ":
    currentNode = followSteps()
    stepCount += 1


print("Steps until ZZZ: " + str(stepCount))  # answer 19199
