from pathlib import Path
filepath = Path(__file__).parent / "input.txt"

with open(filepath, "r") as file:
    lines = [line.strip() for line in file]

potentialGearCoords = []
digitCoords  = []
partNumbers = {}
partNumberIds = {}
potentialGearNumbers = {}

# Create list of coordinates where numbers and * are
for i in range(len(lines)):
    for pos, char in enumerate(lines[i]):
        if char == '.':
            continue
        if char.isdigit():
            digitCoords.append((i, pos))
            continue
        if char == '*':
            potentialGearCoords.append((i, pos))

# Parse part numbers from digit coordinates
for coord in digitCoords:
    if((coord[0], coord[1] - 1)) in digitCoords: #don't process the same number twice
        continue
    number = i = 0
    line = lines[coord[0]]
    thisNumberCoords = []
    while (coord[0], coord[1] + i) in digitCoords: #for each digit
        number = 10 * number + int(line[coord[1] + i]) #generating the part number from individual digits
        thisNumberCoords.append((coord[0], coord[1] + i)) #keep track of coordinates this number occupies
        i += 1
    for thisCoord in thisNumberCoords: #for every coordinate associated with this number
        partNumbers[thisCoord] = len(partNumberIds) #create dictionary entry associating coord with distinct part number id
    partNumberIds[len(partNumberIds)] = number #create list of distinct part number locations but allow duplicate part numbers
    
# For each potential gear, check adjacent (diagonal included) spaces for numbers
for coord in potentialGearCoords:
    adjacents = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for adjacent in adjacents:
        checkCoord = tuple(map(lambda i, j: i + j, coord, adjacent))
        if checkCoord in digitCoords:
            if coord in potentialGearNumbers.keys(): #create list of numbers adjacent to each potential gear, use sets to avoid duplicates
                potentialGearNumbers[coord].add(partNumbers[checkCoord])
            else:
                potentialGearNumbers[coord] = {partNumbers[checkCoord]}

gearRatioSum = 0
for potentialGearNumber in potentialGearNumbers:
    thisGear = potentialGearNumbers[potentialGearNumber]
    if len(thisGear) == 2: #if potential gear has 2 adjacent parts it is a gear
        gearRatioSum += partNumberIds[list(thisGear)[0]] * partNumberIds[list(thisGear)[1]]

print("Gear Ratio Grand Total: " + str(gearRatioSum)) #answer 84363105