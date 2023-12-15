# Need to roll N -> W -> S -> E 1000000000 times so probably need to get efficient
# initial idea, create a mapping for each non-# location to where they will roll for each direction
# this would requre logic for handling bumping into a rock since how many will be in the way will be dynamic
# maybe some sort of multi-threading is possible since each column is independant during a roll
# might be worth it to try to time things
# possibly this is not necessarily. speed test says what exists so far is 0 ns, so 4B*0 = 0 right?

# also need to write code for rolling in other directions
# possibly the easiest thing is to just use the zip function to re-orientate the columns but that might be too time intensive

from pathlib import Path

filepath = Path(__file__).parent / "inputTest.txt"

platform = []
with open(filepath, "r") as file:
    for line in file:
        platform.append(list(line.strip()))  # West is small indexes
rows = platform
cols = [list(x) for x in zip(*platform)]  # columnize, North is small indexes


# all O move down index until blocked by end of list, #, or other O that is already blocked
def roll(lines, rollUp=False):
    rollIndex = None
    if not rollUp:
        for line in lines:
            for i in range(len(line)):
                if line[i] == "." and (rollIndex == None or i < rollIndex):
                    rollIndex = i
                elif line[i] == "#":
                    rollIndex = None
                elif line[i] == "O" and (rollIndex != None and rollIndex < i):
                    line[rollIndex] = "O"
                    line[i] = "."
                    rollIndex += 1
    else:
        for line in lines:
            for i in range(len(line) - 1, -1, -1):
                if line[i] == "." and (rollIndex == None or i > rollIndex):
                    rollIndex = i
                elif line[i] == "#":
                    rollIndex = None
                elif line[i] == "O" and (rollIndex != None and rollIndex > i):
                    line[rollIndex] = "O"
                    line[i] = "."
                    rollIndex -= 1
    return lines


# could be done in roll to decrease looping if needed. Wasn't desireable for Part 2 so good :)
def calculateLoad(col):
    load = 0
    maxLoad = len(col)
    for i in range(len(col)):
        if col[i] == "O":
            load += maxLoad - i
    return load


def cycle(rows, cols):
    cols = roll(cols)  # North
    rows = [list(x) for x in zip(*cols)]

    rows = roll(rows)  # West
    cols = [list(x) for x in zip(*rows)]

    cols = roll(cols, True)  # South
    rows = [list(x) for x in zip(*cols)]

    rows = roll(rows, True)  # East
    cols = [list(x) for x in zip(*rows)]

    return rows, cols


def prettyPrint(rows):
    for row in rows:
        print(" ".join(row))
    print(50 * "-")


totalLoad = 0
cycles = 1000000000
print("Initial")
prettyPrint(rows)
for i in range(cycles):
    rows, cols = cycle(rows, cols)
    # print("Cycle: " + str(i + 1))
    # prettyPrint(rows)

for col in cols:
    load = calculateLoad(col)
    totalLoad += load
    # print(col, load)

print("Total load on north support beams: " + str(totalLoad))  # answer
