from pathlib import Path
from copy import copy
import functools

filepath = Path(__file__).parent / "input.txt"
directions = [(0, -1), (0, 1), (1, 0), (-1, 0)]
areaMap = []
start = (
    1,
    1,
)  # original input start is (0, 1) but it isn't counted in path length. replacing original start w/ # means no out of bounds checking
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


def possibleNext(path):
    current = path[-1]
    # handle slopes
    # if areaMap[current[1]][current[0]] == ">":
    #     return [tuple(map(sum, zip(current, directions[2])))]
    # if areaMap[current[1]][current[0]] == "v":
    #     return [tuple(map(sum, zip(current, directions[1])))]

    possibles = []
    for dir in directions:
        next = tuple(map(sum, zip(current, dir)))
        # already visited or # = rock
        if areaMap[next[1]][next[0]] == "#":
            continue
        if next in path:
            continue
        # if areaMap[next[1]][next[0]] == ">" and dir != (1, 0):
        #     continue
        # if areaMap[next[1]][next[0]] == "v" and dir != (0, 1):
        #     continue
        else:
            possibles.append(next)
    return possibles if possibles else False


# parse map from input
with open(filepath, "r") as file:
    for line in file:
        line = line.strip()
        row = []
        for char in line:
            # Start on the path tile in first row
            # if not start and char == ".":
            #     start = (len(row), 0)
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
    path.append(next)
    possibles = []
    while (not possibles or len(possibles) == 1) and path[-1] != end:
        possibles = possibleNext(path)
        if possibles == False:
            break
        for next in possibles:
            if next == end:
                path.append(next)
                paths.append(path)
                print(
                    f"Paths found: {len(paths)} Longest: {max([len(path) for path in paths])} Current queue: {len(queue)}"
                )
                uniquePaths = set(tuple(path) for path in paths)
                if len(uniquePaths) != len(paths):
                    "DUPLICATE PATH FOUND SOMETHING BAD IS HAPPENING"
                break
            else:
                if len(possibles) > 1:
                    queue.append((path.copy(), next))
                else:
                    path.append(next)

print(
    f"How many steps long is the longest hike? Answer: {max([len(path) for path in paths])}"
)  # answer 5874???
