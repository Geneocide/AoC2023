import numpy as np
from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

directions = {"U": (0, -1), "D": (0, 1), "R": (1, 0), "L": (-1, 0)}
dirCodes = {"0": "R", "1": "D", "2": "L", "3": "U"}
corners = []
xMax, yMax = 0, 0


def getNextCoords(x, y, dir, dis):
    return (x + directions[dir][0] * dis), (y + directions[dir][1] * dis)


# uses shoelace method
def calculateInterior(corners):
    npCorners = np.array(corners, dtype="int64")  # numbers overflow w/ default 32

    npCorners = npCorners.reshape(-1, 2)

    x = npCorners[:, 0]
    y = npCorners[:, 1]

    sum1 = np.sum(x * np.roll(y, 1))
    sum2 = np.sum(y * np.roll(x, 1))

    area = 0.5 * np.absolute(sum1 - sum2)
    return area


perimeter = 0
with open(filepath, "r") as file:
    previousCoords = (0, 0)
    for line in file:
        hexString = line.strip()[line.index("#") + 1 : -1]
        dirCode = hexString[-1]
        dir = dirCodes[dirCode]
        hexDis = hexString[:-1]
        dis = int(hexDis, base=16)
        perimeter += dis
        print(f"{dir} {dis}")
        previousCoords = getNextCoords(*previousCoords, dir, dis)
        corners.append(previousCoords)
    perimeter /= 2  # I think half is taken care of by shoelace? it's expecting math points not pixels with size
    perimeter += 1  # corner point needs counting


area = calculateInterior(corners)
print(f"Total cubic meters of lava: {area + perimeter:.0f}")  # answer 90111113594927
