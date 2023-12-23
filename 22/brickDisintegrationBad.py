from pathlib import Path
import itertools

filepath = Path(__file__).parent / "inputTest.txt"
bricks = []
zMax = 0


def cubesFromEnds(e1, e2):
    global zMax
    x1, y1, z1 = [int(v) for v in e1.split(",")]
    x2, y2, z2 = [int(v) for v in e2.split(",")]
    if max(z1, z2) > zMax:
        if z1 > zMax and z2 > zMax:
            zMax = min(z1, z2)
        else:
            zMax = max(z1, z2)
    brick = set()
    if x1 != x2:
        for x in range(min(x1, x2), max(x1, x2) + 1):
            brick.add((x, y1, z1))
    if y1 != y2:
        for y in range(min(y1, y2), max(y1, y2) + 1):
            brick.add((x1, y, z1))
    if z1 != z2:
        for z in range(min(z1, z2), max(z1, z2) + 1):
            brick.add((x1, y1, z))
    return brick


def moveDown(brick, amount=1):
    newPos = []
    for cube in brick:
        newPos.append((cube[0], cube[1], cube[2] - amount))
    return newPos


def getTop(bricks):
    top = 0
    for brick in bricks:
        for cube in brick:
            if cube[2] > top:
                top = cube[2]
    return top


def allCubesBetween(start_tuple, end_tuple):
    start_tuple = tuple(map(int, start_tuple))
    end_tuple = tuple(map(int, end_tuple))

    # Create a generator that yields all possible tuples between the start and end tuples
    tuples = itertools.product(
        range(start_tuple[0], end_tuple[0] + 1),
        range(start_tuple[1], end_tuple[1] + 1),
        range(start_tuple[2], end_tuple[2] + 1),
    )
    return set(tuples)


def isClearBelow(brick, settled):
    # horizontal
    if brick[0][2] == brick[1][2]:
        cubes = allCubesBetween(*brick).union(brick)
        print(cubes)

        for cube in cubes:
            checkCube = tuple(v1 + v2 for v1, v2 in zip(cube, (0, 0, -1)))
            if any(
                checkCube[0] in range(brick[0][0], brick[1][0] + 1)
                or checkCube[1] in range(brick[0][1], brick[1][1] + 1) in brick
                for brick in settled
            ):
                settled.append(brick)
                return False, settled

    # vertical
    else:
        cube = brick[0] if brick[0][2] < brick[1][2] else brick[1]
        checkCube = tuple(v1 + v2 for v1, v2 in zip(cube, (0, 0, -1)))
        if any(
            checkCube[0] in range(brick[0][0], brick[1][0] + 1)
            or checkCube[1] in range(brick[0][1], brick[1][1] + 1) in brick
            for brick in settled
        ):
            settled.append(brick)
            return False, settled

    return True, settled


def settle(bricks):
    settled = []
    for brick in bricks:
        if any([end[2] == 1 for end in brick]):
            settled.append(brick)
    for z in range(2, zMax + 1):
        print(f"Settled to level {z}")
        for brick in bricks:
            if brick not in settled:
                if any(end[2] == z for end in brick):
                    while brick not in settled:
                        markedClear, settled = isClearBelow(brick, settled)
                        if markedClear:
                            brick = moveDown(brick)
    return settled


def getSupported(brick):
    supported = set()
    for cube in brick:
        aboveCube = list(cube)
        aboveCube[2] += 1
        for b in bricks:
            if b != brick and tuple(aboveCube) in b:
                supported.add(tuple(b))
    return supported if supported else None


# parse map from input
with open(filepath, "r") as file:
    for line in file:
        ends = line.strip().split("~")
        ends = [end.split(",") for end in ends]
        brick = tuple(tuple(int(char) for char in edge) for edge in ends)
        if min(brick[0][2], brick[1][2]) > zMax:
            zMax = min(brick[0][2], brick[1][2])
        bricks.append(brick)

# print(bricks)

bricks = settle(bricks)

# print(bricks)

safeToDestroyBricks = set()
brickSupportingBricks = {}
for brick in bricks:
    supportedBricks = getSupported(brick)
    if supportedBricks:
        brickSupportingBricks[tuple(brick)] = supportedBricks
    else:
        # any brick that supports nothing can be destroyed
        safeToDestroyBricks.add(tuple(brick))
    # print(f"{brick} supports {supportedBricks}")
# print(brickSupportingBricks)

supportedByMultiple = []
for brick in bricks:
    supportedByCount = 0
    for supportedBricks in brickSupportingBricks.values():
        if supportedBricks:
            if tuple(brick) in supportedBricks:
                supportedByCount += 1
                if supportedByCount > 1:
                    supportedByMultiple.append(brick)
    # print(f"{brick} is supported {supportedByCount} time(s)")

# print(supportedByMultiple)

# any brick that supports only bricks that are supported by multiple can be destroyed
for brick in bricks:
    if tuple(brick) not in safeToDestroyBricks:
        supportedBricks = brickSupportingBricks[tuple(brick)]
        if all(list(b) in supportedByMultiple for b in supportedBricks):
            safeToDestroyBricks.add(tuple(brick))

# print(safeToDestroyBricks)

print(
    f"How many bricks could be safely chosen as the one to get disintegrated? Answer: {len(safeToDestroyBricks)}"
)  # answer
