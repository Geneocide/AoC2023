from pathlib import Path

filepath = Path(__file__).parent / "input.txt"
grid = []
colMax = 0
rowMax = 0
connectsNorth = ["|", "L", "J", "S"]
connectsSouth = ["|", "7", "F", "S"]
connectsWest = ["-", "7", "J", "S"]
connectsEast = ["-", "L", "F", "S"]
connections = {
    (-1, 0): connectsNorth,
    (1, 0): connectsSouth,
    (0, -1): connectsWest,
    (0, 1): connectsEast,
}


def isInMap(col, row):
    if col < 0 or row < 0 or col > colMax or row > rowMax:
        return False
    return True


def progress(col, row):
    thisSymbol = grid[row][col]
    for connection in connections:
        if thisSymbol in connections[connection]:
            checkingSymbol = grid[row + connection[0]][col + connection[1]]
            checkingCoords = (col + connection[1], row + connection[0])
            if checkingCoords in pipe or not isInMap(*checkingCoords):
                continue
            if checkingSymbol in connections[(connection[0] * -1, connection[1] * -1)]:
                print(
                    "found connection at: "
                    + str((col + connection[1], row + connection[0]))
                )
                return (col + connection[1], row + connection[0])
    return None


# parse grid and pipe layout
with open(filepath, "r") as file:
    for line in file:
        grid.append(line.strip())

start = None
for row in range(len(grid)):
    for col in range(len(grid[row])):
        if grid[row][col] == "S":
            print("found start at: " + str((col, row)))
            start = (col, row)
rowMax = len(grid)
colMax = len(grid[0])

pipe = [start]
distance = 0
while distance == 0 or nextPipe is not None:
    nextPipe = progress(*pipe[-1])
    distance += 1
    pipe.append(nextPipe)

print(
    "Pipe length: "
    + str(distance)
    + " so furthest from start: "
    + str(int(distance / 2))
)

# this is a bit of a cheat, requires eyeballing the input
grid[start[1]] = grid[start[1]].replace(
    "S", "|"
)  # change S to | because it functions like an | for enclosure purposes
connectsNorth = ["|", "L", "J"]
connectsSouth = ["|", "7", "F"]

# determine inside/outside
# this could maybe be more efficient by finding adjacents. Like, if there's a big patch of inside or outside, rather that doing the normal check just match with what's adjacent
enclosedSpaces = []
crossSymbols = "| 7 J".split()
for row in range(rowMax):
    for col in range(colMax):
        if (col, row) in pipe:
            continue
        else:
            pipeCrosses = 0
            y = row
            for x in range(col + 1, colMax):
                if (x, row) not in pipe:
                    continue
                if y == row:
                    if grid[y][x] == "F":
                        if y == 0:
                            break
                        y -= 1
                    elif grid[y][x] == "L":
                        if y == rowMax - 1:
                            break
                        y += 1
                    elif grid[row][x] in crossSymbols:
                        pipeCrosses += 1
                else:
                    if row < y:
                        if (
                            grid[row][x] in connectsSouth
                            and grid[y][x] in connectsNorth
                        ):
                            pipeCrosses += 1
                    else:
                        if (
                            grid[row][x] in connectsNorth
                            and grid[y][x] in connectsSouth
                        ):
                            pipeCrosses += 1

            if pipeCrosses % 2 != 0:
                print("enclosed found start at: " + str((col, row)))
                enclosedSpaces.append((col, row))

# answer is count of inside spaces
print("Total spaces enclosed: " + str(len(enclosedSpaces)))  # answer 381
