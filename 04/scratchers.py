import re
from pathlib import Path
filepath = Path(__file__).parent / "input.txt"

with open(filepath, "r") as file:
    lines = [line.strip() for line in file]

pointsTotal = 0

for line in lines:
    cardNumberSplit = line.split(":")
    #cardNumber = re.sub("[^0-9]", "", cardNumberSplit[0])
    winningNumbersStr, cardNumbersStr = cardNumberSplit[1].split(" | ")
    winningNumbers = winningNumbersStr.split()
    cardNumbers = cardNumbersStr.split()
    numberMatches = 0
    for cardNumber in cardNumbers:
        if cardNumber in winningNumbers:
            numberMatches += 1
    if numberMatches == 0:
        continue
    points = 1
    for i in range(1, numberMatches):
        points = points * 2
    pointsTotal += points

print("Points Grand Total: " + str(pointsTotal)) #answer 25004