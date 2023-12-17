from collections import defaultdict
from heapq import heappop, heappush
from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

cityMap = []
xMax, yMax = None, None
directions = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
dirChars = {"N": "^", "S": "v", "E": ">", "W": "<"}
# import map as list of lists of characters
with open(filepath, "r") as file:
    for line in file:
        line = line.strip()
        row = []
        for char in line:
            row.append(char)
        cityMap.append(row)
xMax, yMax = len(cityMap[0]), len(cityMap)
start = (0, 0, "E", 0, 0)  # x, y, dir, straightCount, heatLoss
end = (xMax, yMax, None, None, None)


def prettyPrint(cityMap):
    for row in cityMap:
        print(" ".join(row))


def prettyPrintPath(path):
    for y in range(yMax):
        row = []
        for x in range(xMax):
            row.append(cityMap[y][x])
            for i in range(len(path)):
                pathPart = path[i]
                if pathPart[0] == x and pathPart[1] == y:
                    row.pop()
                    row.append(f"\033[42m" + dirChars[pathPart[2]] + f"\033[0m")
                    break
        print(" ".join(row))
    print(50 * "-")


def getPathFromScores(x, y):
    path = []
    while not (x == 0 and y == 0):
        minKey = min(scores[(x, y)].keys(), key=scores[(x, y)].get)
        x, y = getNextCoords(x, y, getOppositeDirection(minKey[0]))
        path.append((x, y, "E" if minKey[0] == "2" else minKey[0]))
    prettyPrintPath(path)


def isInBounds(x, y):
    return not (x < 0 or x >= xMax or y < 0 or y >= yMax)


def getNextCoords(x, y, dir):
    return (x + directions[dir][0]), (y + directions[dir][1])


def calculateStraitCount(heading, straightCount, moveDirection):
    if heading == moveDirection:  # going straight
        return straightCount + 1
    if straightCount >= 4:  # can't turn for minimum of 4
        return 1


# returns direction opposite of one given. Could use direction coordinates but I bet this is faster
def getOppositeDirection(direction):
    if direction == "N":
        return "S"
    if direction == "S":
        return "N"
    if direction == "E":
        return "W"
    if direction == "W":
        return "E"


def dijkstra(start):
    queue = [start]
    scores = {
        (i, j): defaultdict(lambda: float("inf"))
        for j in range(yMax)
        for i in range(xMax)
    }
    while queue:
        x, y, heading, straightCount, heatLoss = heappop(queue)
        for moveDirection in directions:
            newStraightCount = calculateStraitCount(
                heading, straightCount, moveDirection
            )
            # can't go straight more than 10
            if not newStraightCount or newStraightCount > 10:
                continue
            # not allowed to go backwards
            if heading == getOppositeDirection(moveDirection):
                continue
            xNew, yNew = getNextCoords(x, y, moveDirection)
            if isInBounds(xNew, yNew):
                newHeatLoss = heatLoss + int(cityMap[yNew][xNew])
                if newHeatLoss < scores[xNew, yNew][moveDirection, newStraightCount]:
                    scores[xNew, yNew][moveDirection, newStraightCount] = newHeatLoss
                    newElement = (
                        xNew,
                        yNew,
                        moveDirection,
                        newStraightCount,
                        newHeatLoss,
                    )
                    heappush(queue, newElement)
    return scores


scores = dijkstra(start)
minimumHeatLoss = min(
    heatLoss
    for (_, straightCount), heatLoss in scores[xMax - 1, yMax - 1].items()
    if straightCount >= 4  # necessary for rule about stopping at the end
)
print("Minimum heat loss: " + str(minimumHeatLoss))  # answer 1057
