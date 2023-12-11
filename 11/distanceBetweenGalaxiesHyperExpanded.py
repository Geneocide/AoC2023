from operator import sub
from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

expansionValue = 1000000
grid = []
# could use coords as key and make things a little simpler, but I thought maybe harder for human parsing
galaxies = {}
# not really needed, could just calculate as we iterate direction
galaxyPairs = []
expandedRows = []
expandedCols = []
expanded = []


def distanceBetweenTwoPoints(p1, p2):
    c = tuple(map(sub, p1, p2))
    c = map(abs, c)
    answer = sum(c)
    return answer


# def distanceBetweenTwoPoints(p1, p2):
#     c = tuple(map(sub, p1, p2))
#     c = tuple(map(lambda x: x**2, c))
#     answer = sum(c)
#     answer = answer**0.5
#     return answer


# def distanceBetweenTwoPoints(p1, p2):
#     dx, dy = map(sub, p1, p2)
#     steps = max(abs(dx), abs(dy))
#     incrementX = dx / float(steps)
#     incrementY = dy / float(steps)
#     x = round(x + incrementX)
#     y = round(y + incrementY)
#     answer = sum(x, y)
#     return answer


# this could probably made to be a map somehow so that it doesn't take up so much space
# def calculateExpandedCoords(x, y):
#     expandedX = x + sum(expansionValue - 1 for col in expandedCols if col <= x)
#     expandedY = y + sum(expansionValue - 1 for row in expandedRows if row <= y)
#     return (expandedX, expandedY)


# this surprisingly works. it's using x, and y from the for loops below
def calculateExpandedCoords():
    return tuple(
        map(
            lambda lst, coord: coord
            + sum(expansionValue - 1 for val in lst if val <= coord),
            expanded,
            (x, y),
        )
    )


# parse input into an array of arrays
with open(filepath, "r") as file:
    for line in file:
        grid.append(line.strip())
grid.reverse()  # reverse makes it so y increases upwards like standard

# identify rows and columns w/ no galaxies and double them
for i in range(len(grid)):
    if "#" not in grid[i]:
        print("expanding row: " + str(i))
        expandedRows.append(i)
for i in range(len(grid[0])):
    galaxiesPresent = False
    for row in grid:
        if row[i] == "#":
            galaxiesPresent = True
            break
    if not galaxiesPresent:
        print("expanding column: " + str(i))
        expandedCols.append(i)

expanded.append(expandedCols)
expanded.append(expandedRows)
# for each galaxy pair (direction irrelevant) find shortest distance
# find coords of each galaxy and put in dict
for y in range(len(grid)):
    for x in range(len(grid[0])):
        if grid[y][x] == "#":
            galaxies[len(galaxies)] = calculateExpandedCoords()
for i in range(len(galaxies)):
    for j in range(i + 1, len(galaxies)):
        galaxyPairs.append((i, j))
# get distance between each pair
distanceSum = 0
for pair in galaxyPairs:
    distanceSum += distanceBetweenTwoPoints(galaxies[pair[0]], galaxies[pair[1]])

print("Sum of distances between galaxies: " + str(distanceSum))  # answer 685038186836
