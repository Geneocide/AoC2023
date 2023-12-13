from itertools import combinations
import re
from pathlib import Path

filepath = Path(__file__).parent / "inputTest.txt"

data = {}


def generatePossibleSequences(data):
    machines = eliminateUnknowns(data)
    sequence = data[1]
    unknownIndexes = [match.start() for match in re.finditer("[?]", machines)]
    totalBroken = sum(sequence)
    knownBroken = machines.count("#")
    totalUnknown = machines.count("?")
    missingBroken = totalBroken - knownBroken
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


def makeChunks(data):
    machines, sequence = data
    countOfMachinesBetweenKnownWorking = list(
        filter(lambda x: x > 0, map(len, re.split("[.]", machines)))
    )
    chunkedData = []
    for x in countOfMachinesBetweenKnownWorking:
        sequenceTotal = 0
        for i in range(len(sequence)):
            sequenceTotal += sequence[i] + 1
            if sequenceTotal >= x:
                chunkedData.append((machines[:x], sequence[: (i + 1)]))
                machines = machines[(x + 1) :]
                sequence = sequence[(i + 1) :]
                break
    return chunkedData


def eliminateUnknowns(data):
    optimizedMachines = ""
    chunks = makeChunks(data)
    for chunk in chunks:
        machines, sequence = chunk
        while True:
            workingIndexes = []
            unknownIndexes = [match.start() for match in re.finditer("[?]", machines)]
            for i in range(len(unknownIndexes)):
                possibility = machines
                possibility = (
                    possibility[: unknownIndexes[i]]
                    + "#"
                    + possibility[(unknownIndexes[i] + 1) :]
                )
                if (
                    possibility.find("#" * (max(sequence) + 1)) != -1
                ):  # found something impossible
                    workingIndexes.append(unknownIndexes[i])
            if len(workingIndexes) > 0:
                for i in workingIndexes:
                    machines = machines[:i] + "." + machines[i + 1 :]
            else:
                optimizedMachines += machines + "."
                break
    return optimizedMachines


def checkValidity(possibility, sequence):
    if possibility.find("#" * (max(sequence) + 1)) != -1:
        return 0
    groups = list(filter(lambda x: x > 0, map(len, re.split("[.?]", possibility))))
    return groups == sequence


with open(filepath, "r") as file:
    for line in file:
        m, s = line.strip().split()
        mu = m
        su = s
        for i in range(4):
            mu += "?" + m
            su += "," + s
        sequenceList = list(map(int, su.split(",")))
        data[len(data)] = (mu, sequenceList)

totalValidPossibility = 0
for i in range(len(data)):
    validPossibilities = generatePossibleSequences(data[i])
    totalValidPossibility += validPossibilities
    print(str(data[i][0]) + " - " + str(validPossibilities))

print("All possible arrangements: " + str(totalValidPossibility))  # answer
