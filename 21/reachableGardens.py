from pathlib import Path
import copy

filepath = Path(__file__).parent / "input.txt"
uniquePlots = 0
gardenMap = []
steps = 64  # for example do 6 steps (64 for real Part 1 input)
directions = {(0, -1), (0, 1), (1, 0), (-1, 0)}
start = None


def prettyPrint(printMap=gardenMap):
    for row in printMap:
        print(" ".join(row))
    print("-" * 50)


def prettyPrintStep(spots):
    tempMap = copy.deepcopy(gardenMap)
    for x, y in spots:
        tempMap[y][x] = "O"
    prettyPrint(tempMap)


# "#" is a rock and is impassable
# "." is a garden space and can be moved on
# S counts as a reachable garden space
def isSpotClear(x, y, dx, dy):
    if gardenMap[y + dy][x + dx] in ("S", "."):
        return (x + dx, y + dy)


# parse map from input
with open(filepath, "r") as file:
    for line in file:
        line = line.strip()
        row = []
        for char in line:
            # Start on the S
            if char == "S":
                start = (len(row), len(gardenMap))
            row.append(char)
        gardenMap.append(row)

# prettyPrint()

# for each step, track all possible moves, including moving backwards
nextSpots = set()  # count unique garden spaces that are reached
for step in range(steps):
    if step == 0:
        possibleSpots = {start}
    else:
        possibleSpots = nextSpots.copy()
    nextSpots.clear()
    for spot in possibleSpots:
        for dir in directions:
            newSpot = isSpotClear(*spot, *dir)
            if newSpot:
                nextSpots.add(newSpot)
    # print(f"{step+1}")
    # prettyPrintStep(nextSpots)

uniquePlots = len(nextSpots)


print(f"How many garden plots could the Elf reach in exactly 64 steps?")
print(f"Garden plot count: {uniquePlots}")  # answer 3737
# print(f"For example expecting 16 so off by {16 - uniquePlots}")
