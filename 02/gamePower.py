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

powerGrandTotal = 0
powers = []
for gameId in games:
    power = 1
    for color in games[gameId]:
        power = power * games[gameId][color]
    powers.append(power)

for power in powers:
    powerGrandTotal += power

# Print the result
print("Power Grand Total: " + str(powerGrandTotal)) #answer 72227