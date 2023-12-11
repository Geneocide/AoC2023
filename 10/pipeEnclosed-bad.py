from pathlib import Path

filepath = Path(__file__).parent / "inputTest.txt"
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

# determine inside/outside
# find space that is definitely outside
outside = []
while len(outside) == 0:
    for col in range(colMax):
        if grid[0][col] == ".":
            outside.append((col, 0))
    for col in range(colMax):
        if grid[-1][col] == ".":
            outside.append((col, rowMax))
    for row in range(1, rowMax - 1):
        if grid[row][0] == ".":
            outside.append((0, row))
        elif grid[row][-1] == ".":
            outside.append((colMax, row))
# compare east then south alternately until you hit a pipe piece to get an outside reference for the pipe
pipeFound = False
while pipeFound == False:
    if len(outsideCheckCoord) % 2 == 0:
        outsideCheckCoord = (outside[-1][0], outside[-1][1] + 1)
    else:
        outsideCheckCoord = (outside[-1][0] + 1, outside[-1][1])
    if isInMap((outside[-1][0] + 1, outside[-1][1])):
        if outsideCheckCoord in pipe:
            pipeFound == True
        else:
            outside.append(outsideCheckCoord)

# iterate along pipe and check for full spaces that are inside


# answer is count of inside spaces
