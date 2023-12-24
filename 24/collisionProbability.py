from pathlib import Path

filepath = Path(__file__).parent / "input.txt"
areaMin = 200000000000000
areaMax = 400000000000000
# areaMin = 7
# areaMax = 27
vectors = []

with open(filepath, "r") as file:
    for line in file:
        point, velocity = line.strip().split(" @ ")
        point = tuple(int(c) for c in point.split(", "))
        velocity = tuple(int(c) for c in velocity.split(", "))
        vectors.append((point, velocity))


def findIntersection(p1, v1, p2, v2):
    x1, y1, _ = p1
    vx1, vy1, _ = v1
    x2, y2, _ = p2
    vx2, vy2, _ = v2

    if vx1 == vx2 and vy1 == vy2:  # parallel
        return None

    xdiff = (x1 - vx1, x2 - vx2)
    ydiff = (y1 - vy1, y2 - vy2)

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None, None

    d = (det(p1, v1), det(p2, v2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    return (x, y), d


validCount = 0
for i, a in enumerate(vectors):
    a, va = a
    for b in vectors[i + 1 :]:
        b, vb = b
        # print(f"{a} and {b}")
        intersection, d = findIntersection(
            a, tuple(map(sum, zip(a, va))), b, tuple(map(sum, zip(b, vb)))
        )
        if (
            not intersection
            or intersection[0] < areaMin
            or intersection[0] > areaMax
            or intersection[1] < areaMin
            or intersection[1] > areaMax
        ):
            print(f"No valid intersection: {intersection}")
        else:
            dx = intersection[0] - a[0]
            dy = intersection[1] - a[1]
            if not ((dx > 0) == (va[0] > 0) and (dy > 0) == (va[1] > 0)):
                # print("Invalid because intersection in the past")
                continue
            dx = intersection[0] - b[0]
            dy = intersection[1] - b[1]
            if not ((dx > 0) == (vb[0] > 0) and (dy > 0) == (vb[1] > 0)):
                # print("Invalid because intersection in the past")
                continue
            else:
                # print(f"Intersection: {intersection}")
                validCount += 1

print(
    f"How many of these intersections occur within the test area? Answer: {validCount}"
)  # answer 4892 (low), 12015
