from heapq import heappop, heappush
from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

directions = {"U": (0, -1), "D": (0, 1), "R": (1, 0), "L": (-1, 0)}
trenchPath = set()
xMax, yMax, xMin, yMin = 0, 0, 999999999, 999999999


def prettyPrintPath(path, interior=()):
    for y in range(yMin, yMax + 1):
        row = []
        for x in range(xMin, xMax + 1):
            row.append(".")
            for px, py in path:
                if px == x and py == y:
                    row.pop()
                    row.append(f"\033[91m" + "#" + f"\033[0m")
                    break
            for px, py in interior:
                if px == x and py == y:
                    row.pop()
                    row.append(f"\033[91m" + "~" + f"\033[0m")
                    break
        print(" ".join(row))
    print(50 * "-")


def getNextCoords(x, y, dir):
    return (x + directions[dir][0]), (y + directions[dir][1])


# in bounds after expanding for exterior checking algorithm
def isInBounds(x, y):
    return not (x < xMin - 1 or x >= xMax + 1 or y < yMin - 1 or y >= yMax + 1)


def calculateInterior(trenchPath):
    # trenchPath = recenter(trenchPath)
    trenchExterior = set()
    allSpace = set()
    queue = []
    for y in range(yMin - 1, yMax + 2):  # under and overshoot grid
        for x in range(xMin - 1, xMax + 2):
            allSpace.add((x, y))
            # add all of new top and bottom
            if y == yMin - 1 or y == yMax + 1:
                trenchExterior.add((x, y))
                heappush(queue, (x, y))
            else:
                # add new sides
                if x == xMin - 1 or x == xMax + 1:
                    trenchExterior.add((x, y))
                    heappush(queue, (x, y))
    while queue:
        x, y = heappop(queue)
        for dir in directions:
            nextSpace = getNextCoords(x, y, dir)
            if (
                isInBounds(*nextSpace)
                and nextSpace not in trenchExterior
                and nextSpace not in trenchPath
            ):
                heappush(queue, nextSpace)
                trenchExterior.add(nextSpace)
    return allSpace.difference(trenchExterior, trenchPath)


with open(filepath, "r") as file:
    previousCoords = (0, 0)  # seed with 0, 0 at start
    for line in file:
        dir, dis, _ = line.strip().split()
        for i in range(int(dis)):
            nextCoords = getNextCoords(*previousCoords, dir)
            previousCoords = nextCoords  # for next iteration

            # keep track of borders of grid
            if nextCoords[0] > xMax:
                xMax = nextCoords[0]
            if nextCoords[1] > yMax:
                yMax = nextCoords[1]
            if nextCoords[0] < xMin:
                xMin = nextCoords[0]
            if nextCoords[1] < yMin:
                yMin = nextCoords[1]
            trenchPath.add((nextCoords))

print(f"Trench perimeter: {len(trenchPath)}")
# prettyPrintPath(trenchPath)

trenchInterior = calculateInterior(trenchPath)
print(f"Trench interior: {len(trenchInterior)}")
# prettyPrintPath(trenchPath, trenchInterior)
print(
    f"Total cubic meters of lava: {len(trenchPath) + len(trenchInterior)}"
)  # answer 40745
