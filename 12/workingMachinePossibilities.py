from itertools import combinations
import re
from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

data = {}


def generatePossibleSequences(machines):
    unknownIndexes = [match.start() for match in re.finditer("[?]", machines)]
    brokenCombos = combinations(range(totalUnknown), missingBroken)
    validPossibilities = 0
    for brokenCombo in brokenCombos:
        possibility = machines
        for i in brokenCombo:
            possibility = (
                possibility[: unknownIndexes[i]]
                + "#"
                + possibility[(unknownIndexes[i] + 1) :]
            )
        validPossibilities += checkValidity(possibility, sequence)
    return validPossibilities


def checkValidity(possibility, sequence):
    groups = list(filter(lambda x: x > 0, map(len, re.split("[.?]", possibility))))
    return groups == sequence


with open(filepath, "r") as file:
    for line in file:
        m, s = line.strip().split()
        sequenceList = list(map(int, s.split(",")))
        data[len(data)] = (m, sequenceList)

totalValidPossibility = 0
for i in range(len(data)):
    machines = data[i][0]
    sequence = data[i][1]
    totalBroken = sum(sequence)
    knownBroken = machines.count("#")
    totalUnknown = machines.count("?")
    missingBroken = totalBroken - knownBroken
    validPossibilities = generatePossibleSequences(machines)
    totalValidPossibility += validPossibilities
    print(machines + " - " + str(validPossibilities))

print("All possible arrangements: " + str(totalValidPossibility))  # answer 7460
