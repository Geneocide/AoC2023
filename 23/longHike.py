from pathlib import Path
from copy import copy
from collections import defaultdict

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


def possibleNext(current, path):
    x, y = current
    possibles = []
    for next in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
        # next = tuple(map(sum, zip(current, dir)))
        # already visited or # = rock
        if areaMap[next[1]][next[0]] == "#":
            continue
        if next in path:
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
            # if not start and char == ".":
            #     start = (len(row), 0)
            row.append(char)
        areaMap.append(row)
xMax = len(areaMap[0])
yMax = len(areaMap)
for i, c in enumerate(areaMap[-1]):
    if c == ".":
        end = (i, len(areaMap) - 1)

queue = [(start, start, {start, (0, 1)})]
graph = defaultdict(list)
# make graph
while queue:
    current, previousNode, path = queue.pop()
    if current == end:
        endNode = previousNode
        finalSteps = len(path) - 1
        continue

    possibles = possibleNext(tuple(current), path)
    # not intersection or dead end
    if len(possibles) == 1:
        next = possibles.pop()
        queue.append((next, previousNode, path | {next}))
    # intersection found
    elif len(possibles) > 1:
        steps = len(path) - 1
        # already found
        if (current, steps) in graph[previousNode]:
            continue
        graph[previousNode].append((current, steps))
        graph[current].append((previousNode, steps))
        # start new paths from current
        while possibles:
            next = possibles.pop()
            queue.append((next, current, {current, next}))

# traverse graph
maxSteps = 0
pathCount = 0
queue = [(start, 0, {start})]
while queue:
    current, steps, path = queue.pop()
    if current == endNode:
        maxSteps = max(steps, maxSteps)
        pathCount += 1
        print(
            f"Paths found: {pathCount} Longest: {maxSteps + finalSteps} Current queue: {len(queue)}"
        )
        continue
    for next, distance in graph[current]:
        if next not in path:
            queue.append((next, steps + distance, path | {next}))

print(
    f"How many steps long is the longest hike? Answer: {maxSteps + finalSteps}"
)  # answer 6398
