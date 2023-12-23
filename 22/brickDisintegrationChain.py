from collections import defaultdict, deque
from pathlib import Path

filepath = Path(__file__).parent / "inputTest.txt"
bricks = []


def fillBricks(data):
    return [
        {
            (x, y, z)
            for x in range(x1, x2 + 1)
            for y in range(y1, y2 + 1)
            for z in range(z1, z2 + 1)
        }
        for (x1, y1, z1), (x2, y2, z2) in data
    ]


def isAtBottom(brick):
    return any(pos[-1] == 0 for pos in brick)


def settle(bricks):
    occupied = {}
    supports = {i: set() for i in range(len(bricks))}
    for i, brick in enumerate(bricks):
        next_pos = {(x, y, z - 1) for x, y, z in brick}
        intersected = {occupied[pos] for pos in next_pos if pos in occupied}
        while not intersected and not isAtBottom(next_pos):
            brick = next_pos
            next_pos = {(x, y, z - 1) for x, y, z in brick}
            intersected = {occupied[pos] for pos in next_pos if pos in occupied}
        occupied |= {pos: i for pos in brick}
        for parent in intersected:
            supports[parent].add(i)
    return supports


def supportedBricks(supports):
    supported = defaultdict(set)
    for parent, children in supports.items():
        for child in children:
            supported[child].add(parent)
    return supported


def cascade(supports, supported, unsafe):
    count = 0
    removed = set()
    queue = deque([unsafe])
    while queue:
        current = queue.popleft()
        removed.add(current)
        for child in supports[current]:
            if not supported[child] - removed:
                count += 1
                queue.append(child)
    return count


# parse input
with open(filepath, "r") as file:
    for line in file:
        ends = line.strip().split("~")
        ends = [end.split(",") for end in ends]
        brick = tuple(tuple(int(char) for char in edge) for edge in ends)
        bricks.append(brick)

bricks.sort(key=lambda brick: brick[0][2])
bricks = fillBricks(bricks)
supports = settle(bricks)
supported = supportedBricks(supports)
safe = {
    parent
    for parent, children in supports.items()
    if not children or all(len(supported[child]) > 1 for child in children)
}
unsafe = set(range(len(bricks))) - safe
total = sum(cascade(supports, supported, brick) for brick in unsafe)

print(
    f"What is the sum of the number of other bricks that would fall? Answer: {total}"
)  # answer 61920
