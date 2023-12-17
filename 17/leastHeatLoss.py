import functools
from pathlib import Path

filepath = Path(__file__).parent / "inputTest.txt"

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

xMax, yMax = len(cityMap[0]) - 1, len(cityMap) - 1
start = (0, 0, "E", 0)
end = (xMax, yMax, None, None)
lowestHeatLoss = 9999999999


def prettyPrint(cityMap):
    for row in cityMap:
        print(" ".join(row))


def prettyPrintPath(path):
    for y in range(yMax + 1):
        row = []
        for x in range(xMax + 1):
            row.append(cityMap[y][x])
            for i in range(len(path)):
                pathPart = path[i]
                if pathPart[0] == x and pathPart[1] == y:
                    row.pop()
                    row.append(f"\033[42m" + dirChars[pathPart[2]] + f"\033[0m")
                    break
        print(" ".join(row))
    print(50 * "-")


def calculateHeatLoss(path):
    heatLoss = 0
    for part in path:
        x = part[0]
        y = part[1]
        heatLoss += int(cityMap[y][x])
    return heatLoss


def isInBounds(x, y):
    return not (x < 0 or x > xMax or y < 0 or y > yMax)


def getNextCoords(x, y, dir, straightCount):
    return ((x + directions[dir][0]), (y + directions[dir][1]), dir, straightCount)


# determine which way is to the goal (can't be N or W)
def getDirectionToEnd(x, y):
    xDelta = end[0] - x
    yDelta = end[1] - y
    if xDelta > yDelta:
        return "E"
    return "S"


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


@functools.cache
def getPossibleMoves(x, y, direction, straightCount):
    movesOrder = ["S", "E", "W", "N"]  # basic move priority order
    movesOrder.remove(
        getOppositeDirection(direction)
    )  # can't go backwards, works for starting case too since we're in a corner
    directionToEnd = getDirectionToEnd(x, y)
    # swap move priority based on direction to end
    if directionToEnd == "E":
        a, b = 0, 1
        movesOrder[b], movesOrder[a] = movesOrder[a], movesOrder[b]
    # can't go straight more than 3
    if straightCount == 3:
        movesOrder.remove(direction)
    validMoves = []
    for moveDirection in movesOrder:
        if moveDirection == direction:
            straightCount += 1
        possibleMove = getNextCoords(x, y, moveDirection, straightCount)
        if possibleMove not in path and isInBounds(possibleMove[0], possibleMove[1]):
            validMoves.append(possibleMove)
    return validMoves


def progress(path):
    global lowestHeatLoss
    if calculateHeatLoss(path) > lowestHeatLoss:  # not going to be best
        return path[:-1]
    if path[-1][0] == end[0] and path[-1][1] == end[1]:  # end found
        print("found a path to the end")
        prettyPrintPath(path)
        heatLoss = calculateHeatLoss(path)
        if heatLoss < lowestHeatLoss:
            lowestHeatLoss = heatLoss
        return path[:-1]

    possibleMoves = getPossibleMoves(*path[-1])
    for move in possibleMoves:
        path += (move,)
        path = progress(path)
    return path[:-1]


prettyPrint(cityMap)
path = (start,)

path = progress(path)

print("Minimum heat loss: " + str(lowestHeatLoss))  # answer
