from pathlib import Path
import copy

filepath = Path(__file__).parent / "input.txt"
directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
areaMap = []
start = None
end = None
xMax = 99999
yMax = 99999


def prettyPrint(printMap=areaMap):
    for row in printMap:
        print(" ".join(row))
    print("-" * 50)


def prettyPrintPath(path):
    tempMap = copy.deepcopy(areaMap)
    for x, y in path:
        if (x, y) == start:
            tempMap[y][x] = "S"
        else:
            tempMap[y][x] = "O"
    prettyPrint(tempMap)


def isInBounds(x, y):
    return not (x < 0 or x >= xMax + 1 or y < 0 or y >= yMax + 1)


def possibleNext(path):
    current = path[-1]
    # handle slopes
    if areaMap[current[1]][current[0]] == ">":
        return [tuple(map(sum, zip(current, directions[2])))]
    if areaMap[current[1]][current[0]] == "v":
        return [tuple(map(sum, zip(current, directions[1])))]

    possibles = []
    for dir in directions:
        next = tuple(map(sum, zip(current, dir)))
        # already visited or # = rock
        if next in path or areaMap[next[1]][next[0]] == "#":
            continue
        if areaMap[next[1]][next[0]] == ">" and dir != (1, 0):
            continue
        if areaMap[next[1]][next[0]] == "v" and dir != (0, 1):
            continue
        else:
            possibles.append(next)
    return possibles


# parse map from input
with open(filepath, "r") as file:
    for line in file:
        line = line.strip()
        row = []
        for char in line:
            # Start on the path tile in first row
            if not start and char == ".":
                start = (len(row), 0)
            row.append(char)
        areaMap.append(row)
xMax = len(areaMap[0])
yMax = len(areaMap)
for i, c in enumerate(areaMap[-1]):
    if c == ".":
        end = (i, len(areaMap) - 1)

visited = []
queue = [([], start)]
paths = []
while queue:
    path, next = queue.pop()
    newPath = path.copy()
    newPath.append(next)
    possibles = possibleNext(newPath)
    for next in possibles:
        if next == end:
            newPath.append(next)
            paths.append(newPath)
        else:
            queue.append((newPath.copy(), next))

print(
    f"How many steps long is the longest hike? Answer: {max([len(path) for path in paths]) - 1}"
)  # answer 2238
