from pathlib import Path

filepath = Path(__file__).parent / "inputTest.txt"

grid = []  # holds input, Y increases downwards, X increase rightwards
colMax = 0
rowMax = 0
connectsNorth = ["|", "L", "J", "S"]
connectsSouth = ["|", "7", "F", "S"]
connectsWest = ["-", "7", "J", "S"]
connectsEast = ["-", "L", "F", "S"]


# create custom object to hold pipe data
class Space(object):
    row = None
    col = None
    coords = None
    symbol = None
    connections = []
    distance = None
    connected = None

    def __init__(self, row, col, symbol):
        self.row = row
        self.col = col
        self.symbol = symbol
        if symbol == "S":
            self.distance = 0
            self.connected = True

    def __repr__(self):
        return self.symbol

    def getAdjacents(self):
        modifiers = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        adjacents = []
        for modifier in modifiers:
            col = self.col + modifier[0]
            row = self.row + modifier[1]
            if col < 0 or row < 0 or col > colMax or row > rowMax:
                continue  # out of bounds
            else:
                adjacents.append(grid[row][col])
        return adjacents

    # determines connections from symbol
    def findConnections(self):
        adjacents = self.getAdjacents()
        toConnect.remove(self)
        for adjacent in adjacents:
            if adjacent in self.connections:
                continue
            if adjacent.symbol == ".":
                adjacent.connected = False
                continue
            if adjacent.distance is not None and adjacent.distance > self.distance:
                # done?
                return self.distance
            if adjacent.symbol in connectsSouth and self.symbol in connectsNorth:
                if adjacent.row == self.row - 1 or self.symbol == "S":
                    self.connect(adjacent)
            elif adjacent.symbol in connectsNorth and self.symbol in connectsSouth:
                if adjacent.row == self.row + 1 or self.symbol == "S":
                    self.connect(adjacent)
            elif adjacent.symbol in connectsEast and self.symbol in connectsWest:
                if adjacent.col == self.col - 1 or self.symbol == "S":
                    self.connect(adjacent)
            elif adjacent.symbol in connectsWest and self.symbol in connectsEast:
                if adjacent.col == self.col + 1 or self.symbol == "S":
                    self.connect(adjacent)
            else:
                adjacent.connected = False
        return self.distance

    def connect(self, adjacent):
        adjacent.connected = True
        adjacent.distance = self.distance + 1
        adjacent.connections.append(self)
        # self.connections.append(adjacent)
        toConnect.add(adjacent)


# parse grid and pipe layout
with open(filepath, "r") as file:
    y = 0
    for line in file:
        row = []
        for x in range(len(line.strip())):
            row.append(Space(y, x, line[x]))
            if y > rowMax:
                rowMax = y
            if x > colMax:
                colMax = x
        y += 1
        grid.append(row)

# starting at S pipe, count only attached pipe pieces
distance = 0
toConnect = set()
for row in grid:
    for space in row:
        if not space.connected:
            continue
        else:
            toConnect.add(space)
            while len(toConnect) > 0:
                d = next(iter(toConnect)).findConnections()
                if d > distance:
                    distance = d

print("Maximum distance: " + str(distance))  # answer
