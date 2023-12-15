from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

platform = []
with open(filepath, "r") as file:
    for line in file:
        platform.append(line.strip())


# all O move down index until blocked by end of list, #, or other O that is already blocked
def roll(col):
    maxRollIndex = None
    for i in range(0, len(col)):
        if col[i] == "." and (maxRollIndex == None or i < maxRollIndex):
            maxRollIndex = i
        elif col[i] == "#":
            maxRollIndex = None
        elif col[i] == "O" and (maxRollIndex != None and maxRollIndex < i):
            col[maxRollIndex] = "O"
            col[i] = "."
            maxRollIndex += 1
    return col


# could be done in roll to decrease looping if needed
def calculateLoad(col):
    load = 0
    maxLoad = len(col)
    for i in range(len(col)):
        if col[i] == "O":
            load += maxLoad - i
    return load


platform = [list(x) for x in zip(*platform)]  # columnize
# print(platform)

totalLoad = 0
for col in platform:
    col = roll(col)
    load = calculateLoad(col)
    totalLoad += load
    # print(col, load)

print("Total load on north support beams: " + str(totalLoad))  # answer 106990
