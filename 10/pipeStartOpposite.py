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


def progress(col, row):
    thisSymbol = grid[row][col]
    for connection in connections:
        if thisSymbol in connections[connection]:
            checkingSymbol = grid[row + connection[0]][col + connection[1]]
            checkingCoords = (col + connection[1], row + connection[0])
            if (
                checkingCoords in pipe
                or checkingCoords[0] < 0
                or checkingCoords[1] < 0
                or checkingCoords[0] > colMax
                or checkingCoords[1] > rowMax
            ):
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
)  # answer 6717
