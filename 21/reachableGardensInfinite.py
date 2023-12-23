from pathlib import Path
import numpy as np

filepath = Path(__file__).parent / "input.txt"
gardenMap = []
steps = 50
directions = {(0, -1), (0, 1), (1, 0), (-1, 0)}
start = None
mapSize = None


# "#" is a rock and is impassable
# "." is a garden space and can be moved on
# S counts as a reachable garden space
def isSpotClear(spot, dir):
    checkSpot = tuple(v1 + v2 for v1, v2 in zip(spot, dir))
    if checkSpot not in visited:
        normalSpot = tuple(v % mapSize for v in checkSpot)  # translate infinite map
        if gardenMap[normalSpot[1]][normalSpot[0]] in ("S", "."):  # check for rocks
            return checkSpot  # return actual coordinates, not normalized, for tracking uniques


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

mapSize = len(gardenMap)
# since the map is repeating, this is the number of repeats we would cross in the number of steps requested
tiles = (26501365 - (len(gardenMap) // 2)) // len(gardenMap)
# steps = 2 * mapSize

# prettyPrint()
breakPoints = (mapSize // 2, mapSize // 2 + mapSize, mapSize // 2 + (2 * mapSize))
answers = {}
# for each step, track all possible moves, including moving backwards
visited = set()
nextSpots = set()  # count unique garden spaces that are reached
possibleSpots = {start}
for step in range(max(breakPoints) + 1):
    if nextSpots:
        possibleSpots = nextSpots.copy()
    nextSpots.clear()
    for spot in possibleSpots:
        for dir in directions:
            newSpot = isSpotClear(spot, dir)
            if newSpot:
                nextSpots.add(newSpot)
    visited = visited.union(nextSpots)
    if step in breakPoints:
        answers[step] = len([(x, y) for x, y in visited if (x + y) % 2 == step % 2])

print(answers)
coefficients = np.polyfit([0, 1, 2], list(answers.values()), 2)
result = np.polyval(coefficients, tiles)
print(np.round(result, 0))

print(f"How many garden plots could the Elf reach in exactly 26501365 steps?")
print(
    f"Garden plot count: {np.round(result, 0):.0f}"
)  # answer 301620878258266 (low), 1240328848015237 (high), 312384314895496 (low), 323188591455496 (wrong), 638110161039201 (wrong), 625382480005896
