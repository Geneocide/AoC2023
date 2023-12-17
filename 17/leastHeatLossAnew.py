from pathlib import Path

filepath = Path(__file__).parent / "inputTest.txt"

cityMap = []
xMax, yMax = None, None
directions = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
dirChars = {"N": "^", "S": "v", "E": ">", "W": "<"}
# import map as list of lists of characters
with open(filepath, "r") as file:
    for line in file:
        line = line.strip()
        row = []
        for char in line:
            row.append(char)
        cityMap.append(row)

xMax, yMax = len(cityMap[0]) - 1, len(cityMap) - 1
start = (0, 0, "E", 0)
end = (xMax, yMax, None, None)
lowestHeatLoss = 9999999999


def prettyPrint(cityMap):
    for row in cityMap:
        print(" ".join(row))


def prettyPrintPath(path):
    for y in range(yMax + 1):
        row = []
        for x in range(xMax + 1):
            row.append(cityMap[y][x])
            for i in range(len(path)):
                pathPart = path[i]
                if pathPart[0] == x and pathPart[1] == y:
                    row.pop()
                    row.append(dirChars[pathPart[2]])
                    break
        print(" ".join(row))


def calculateHeatLoss(path):
    heatLoss = 0
    for part in path:
        x = part[0]
        y = part[1]
        heatLoss += int(cityMap[y][x])
    return heatLoss


def isInBounds(x, y):
    return not (x < 0 or x > xMax or y < 0 or y > yMax)


def min_sum_path_dp(grid, start, end):
    m, n = len(grid), len(grid[0])
    dp = [[float("inf")] * n for _ in range(m)]
    dp[start[0]][start[1]] = 0

    for i in range(m):
        for j in range(n):
            for dir in directions:
            if i > 0:
                dp[i][j] = min(dp[i][j], dp[i - 1][j] + int(grid[i][j]))
            if j > 0:
                dp[i][j] = min(dp[i][j], dp[i][j - 1] + int(grid[i][j]))

    # Backtrack to find the actual path
    path = []
    i, j, xxx, yyy = end
    while i >= 0 and j >= 0:
        path.append((i, j))
        if i > 0 and dp[i - 1][j] <= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return dp[end[0]][end[1]], path


min_sum, path = min_sum_path_dp(cityMap, start, end)
print(f"Minimum sum: {min_sum}")
prettyPrintPath(path)
