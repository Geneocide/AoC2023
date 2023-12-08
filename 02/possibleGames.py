import re
from pathlib import Path
filepath = Path(__file__).parent / "input.txt"

# Read input from the file and strip out non-digits
with open(filepath, "r") as file:
    games = {}
    for line in file:
        line = line.strip()
        lineData = line.split(":") # Game id on left, cube counts on right
        gameId = re.sub("[^0-9]", "", lineData[0]) # strip out non-digits
        draws = lineData[1].split(";")
        colorCounts = {"red": 0, "green": 0, "blue": 0}
        for draw in draws:
            colors = draw.split(",")
            for color in colors:
                for key in colorCounts:
                    if key in color:
                        colorCounts[key] = max(int(re.sub("[^0-9]", "", color)), colorCounts[key])
        games[gameId] = colorCounts

gameIdTotal = 0
for gameId in games:
    if games[gameId]["red"] > 12:
        continue
    if games[gameId]["green"] > 13:
        continue
    if games[gameId]["blue"] > 14:
        continue
    gameIdTotal += int(gameId)

# Print the result
print("Game ID Total: " + str(gameIdTotal)) #answer 224 (low), 2716