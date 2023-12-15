from pathlib import Path


filepath = Path(__file__).parent / "input.txt"

platform = []
stucks = []
rollers = []
northMap, westMap, southMap, eastMap = [], [], [], []
maxRow = 0
maxCol = 0
maps = {"N": northMap, "W": westMap, "S": southMap, "E": eastMap}
positions = []  # list to hold tuples of positions of all the moving rocks


def prettyPrint(rollers):
    for i in range(maxRow):
        row = ""
        for j in range(len(line)):
            char = "."
            if (i, j) in stucks:
                char = "#"
            elif (i, j) in rollers:
                char = "O"
            row += char
        print(" ".join(row))
    print(50 * "-")


with open(filepath, "r") as file:
    for line in file:
        platform.append(list(line.strip()))  # West is small indexes
        maxRow += 1
maxCol = len(platform[0])

for i in range(maxRow):
    for map in maps:
        maps[map].append([])
    for j in range(maxCol):
        if platform[i][j] == "#":
            stucks.append((i, j))
        for map in maps:
            maps[map][-1].append(None)


for i in range(len(platform)):
    for j in range(maxCol):
        if platform[i][j] in ("O", "."):
            westMap[i][j] = (i, 0)
            for k in range(j - 1, -1, -1):
                if (i, k) in stucks:
                    westMap[i][j] = (i, k + 1)
                    break

            eastMap[i][j] = (i, maxCol - 1)
            for k in range(j, maxRow):
                if (i, k) in stucks:
                    eastMap[i][j] = (i, k - 1)
                    break

            northMap[i][j] = (0, j)
            for k in range(i - 1, -1, -1):
                if (k, j) in stucks:
                    northMap[i][j] = (k + 1, j)
                    break

            southMap[i][j] = (maxRow - 1, j)
            for k in range(i, maxCol):
                if (k, j) in stucks:
                    southMap[i][j] = (k - 1, j)
                    break

        if platform[i][j] == "O":
            rollers.append((i, j))

positions.append(tuple(rollers))


def tilt(mapName, rollers):
    actualMap = maps[mapName]
    directionModifier = 1 if mapName in ("N", "W") else -1
    newRollers = []
    for roller in rollers:
        desiredRow, desiredCol = actualMap[roller[0]][roller[1]]
        while (desiredRow, desiredCol) in newRollers:
            if mapName in ("E", "W"):
                desiredCol += 1 * directionModifier
            else:
                desiredRow += 1 * directionModifier
        newRollers.append((desiredRow, desiredCol))
    return newRollers


def cycle(rollers):
    for map in maps:
        # print("Tilting: " + map)
        rollers = tilt(map, rollers)
        # prettyPrint(rollers)
    return rollers


# prettyPrint(rollers)


totalLoad = 0
cycles = 1000
for i in range(cycles):
    rollers = cycle(rollers)
    if tuple(rollers) in positions:
        print(
            "WE'VE BEEN HERE BEFORE!!! Cycle #"
            + str(i)
            + " is the same as "
            + str(positions.index(tuple(rollers)))
        )
    else:
        positions.append(tuple(rollers))
    # print("After " + str(i + 1) + " cycles")
    # prettyPrint(rollers)
    if (i + 1) % 10 == 0:
        print("Cycle: " + str(i + 1))

for roller in rollers:
    totalLoad += maxRow - roller[0]

print("Total load on north support beams: " + str(totalLoad))  # answer 100531
