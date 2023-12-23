from pathlib import Path
import copy

filepath = Path(__file__).parent / "input.txt"
gardenMap = []
steps = 131
directions = {(0, -1), (0, 1), (1, 0), (-1, 0)}
start = None
mapSize = None


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
def isSpotClear(spot, dir):
    checkSpot = tuple(v1 + v2 for v1, v2 in zip(spot, dir))
    normalSpot = tuple(v % mapSize for v in checkSpot)  # translate infinite map
    if gardenMap[normalSpot[1]][normalSpot[0]] in ("S", "."):  # check for rocks
        return (
            checkSpot  # return actual coordinates, not normalized, for tracking uniques
        )


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

# for each step, track all possible moves, including moving backwards
nextSpots = set()  # count unique garden spaces that are reached
oddSpots = set()
evenSpots = set()
oddCorners = set()
evenCorners = set()
possibleSpots = {start}
for step in range(mapSize):
    if nextSpots:
        possibleSpots = nextSpots.copy()
    print(f"step: {step} has a max X of {max(v for v, _ in possibleSpots)}")
    if step % 2 == 0:
        if step > steps // 2:
            evenCorners.union(possibleSpots)
        else:
            evenSpots = evenSpots.union(possibleSpots)
    else:
        if step > steps // 2:
            oddCorners.union(possibleSpots)
        else:
            oddSpots = oddSpots.union(possibleSpots)
    nextSpots.clear()
    for spot in possibleSpots:
        for dir in directions:
            newSpot = isSpotClear(spot, dir)
            if newSpot:
                nextSpots.add(newSpot)
    # print(f"{step+1}")
    # prettyPrintStep(nextSpots)

# for every tile length we cross we square the number of tiles we could reach
# each tile is either reachable via odd or even number of steps and will be filled as such
# so we can count those from the start to the edge and extrapolate
# there are also corners to consider
# In our case the number of tiles we're traveling is even so we have
# (n+1)^2 odd + n^2 even - (n-1) odd corners + n even corners
wholeOdds = (tiles + 1) * (tiles + 1) * len(oddSpots)
wholeEvens = tiles * tiles * len(evenSpots)
cornerOdds = (tiles - 1) * len(oddCorners)
cornerEvens = tiles * len(evenCorners)
uniquePlots = wholeOdds + wholeEvens - cornerOdds + cornerEvens


print(f"How many garden plots could the Elf reach in exactly 26501365 steps?")
print(
    f"Garden plot count: {uniquePlots}"
)  # answer 301620878258266 (low), 1240328848015237 (high), 312384314895496 (low)
# print(f"For example expecting 16 so off by {16 - uniquePlots}")
