from operator import sub
from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

grid = []
# could use coords as key and make things a little simpler, but I thought maybe harder for human parsing
galaxies = {}
galaxyPairs = []


def distanceBetweenTwoPoints(p1, p2):
    c = tuple(map(sub, p1, p2))
    c = map(abs, c)
    answer = sum(c)
    return answer


# parse input into an array of arrays
with open(filepath, "r") as file:
    for line in file:
        grid.append(line.strip())
grid.reverse()  # reverse makes it so y increases upwards like standard

# identify rows and columns w/ no galaxies and double them
for i in range(
    len(grid) - 1, 0, -1
):  # iterate backwards so doubling get in the way of the iteration
    if "#" not in grid[i]:
        print("doubling row: " + str(i))
        grid.insert(i, grid[i])  # double row
for i in range(
    len(grid[0]) - 1, 0, -1
):  # iterate backwards so doubling get in the way of the iteration
    galaxiesPresent = False
    for row in grid:
        if row[i] == "#":
            galaxiesPresent = True
            break
    if not galaxiesPresent:
        print("doubling column: " + str(i))
        for j in range(len(grid)):  # double column
            grid[j] = grid[j][:i] + "." + grid[j][i:]
# for each galaxy pair (direction irrelevant) find shortest distance
# find coords of each galaxy and put in dict
for y in range(len(grid)):
    for x in range(len(grid[0])):
        if grid[y][x] == "#":
            galaxies[len(galaxies)] = (x, y)
for i in range(len(galaxies)):
    for j in range(i + 1, len(galaxies)):
        galaxyPairs.append((i, j))
# get distance between each pair
distanceSum = 0
for pair in galaxyPairs:
    distanceSum += distanceBetweenTwoPoints(galaxies[pair[0]], galaxies[pair[1]])

print("Sum of distances between galaxies: " + str(distanceSum))  # answer 9556896
