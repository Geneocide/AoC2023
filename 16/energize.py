from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

contraption = []
xMax = None
yMax = None
directions = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
# import map as list of lists of characters
with open(filepath, "r") as file:
    for line in file:
        line = line.strip()
        row = []
        for char in line:
            row.append(char)
        contraption.append(row)

xMax = len(contraption[0]) - 1
yMax = len(contraption) - 1


def prettyPrint(contraption):
    for row in contraption:
        print(" ".join(row))


# make a nice grid of # for coordinates in list and '.' for those missing to tell if we match example
def prettyPrintVisited(done):
    for y in range(yMax + 1):
        row = []
        for x in range(xMax + 1):
            if any(t[0] == x and t[1] == y for t in done):
                row.append("#")
            else:
                row.append(".")
        print(" ".join(row))


# prettyPrint(contraption)
# need to know the current square and the current direction
current = (-1, 0, "E")
done = set()
tilesEnergized = set()


def getNextCoords(x, y, dir):
    return ((x + directions[dir][0]), (y + directions[dir][1]), dir)


def updateDirection(x, y, dir):
    if not isInBounds(x, y):
        return [(x, y, dir)]
    char = contraption[y][x]
    if char == ".":
        return [(x, y, dir)]
    if char == "/":
        if dir == "E":
            return [(x, y, "N")]
        if dir == "S":
            return [(x, y, "W")]
        if dir == "N":
            return [(x, y, "E")]
        if dir == "W":
            return [(x, y, "S")]
    if char == "\\":
        if dir == "E":
            return [(x, y, "S")]
        if dir == "S":
            return [(x, y, "E")]
        if dir == "N":
            return [(x, y, "W")]
        if dir == "W":
            return [(x, y, "N")]
    if char == "-":
        if dir in ("E", "W"):
            return [(x, y, dir)]
        else:
            return [(x, y, "E"), (x, y, "W")]
    if char == "|":
        if dir in ("N", "S"):
            return [(x, y, dir)]
        else:
            return [(x, y, "N"), (x, y, "S")]


def isInBounds(x, y):
    return not (x < 0 or x > xMax or y < 0 or y > yMax)


# maybe create a recursive function for moving the light beam
# given current status figure out where it will go (could be multiple)
# base case would be leaving the map OR entering a status that has already been calculated


def progress(current):
    next = getNextCoords(*current)
    next = updateDirection(*next)
    while len(next) < 2:
        if (current[0], current[1]) not in tilesEnergized:
            tilesEnergized.add((current[0], current[1]))
        done.add(current)
        next = getNextCoords(*current)
        next = updateDirection(*next)
        job = next[0]
        if not isInBounds(job[0], job[1]) or job in done:
            break
        else:
            current = job
    for job in next:
        if not isInBounds(job[0], job[1]) or job in done:
            continue
        progress(job)


progress(current)
# print(done)
# prettyPrintVisited(done)

# this removes the initial out of bounds tile I add at the very start, should only be 1
for tile in tilesEnergized:
    x, y = tile
    if not isInBounds(x, y):
        tilesEnergized.remove(tile)
        break

print("Total tiles energized: " + str(len(tilesEnergized)))  # answer 6740
