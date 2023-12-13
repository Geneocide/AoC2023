from itertools import combinations
import re
from pathlib import Path
import functools


filepath = Path(__file__).parent / "inputTest.txt"

data = {}
answer = {}

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


def partition(machines, sequence):
    return [[machines, sequence]]
    machines = re.sub(r"\.\.+", ".", machines.strip("."))
    machineParts = re.split("[.]", machines)
    chunkedData = []
    partsToSkip = []

    for i in range(len(machineParts)):
        if len(machineParts[i]) == sequence[i]:
            chunkedData.append([machineParts[i], [sequence[i]]])
        elif len(machineParts[i]) == 2 and sequence[i] == 1:
            chunkedData.append([machineParts[i], [sequence[i]]])
        else:
            chunkedData.append([".".join(machineParts[i:]), sequence])
            return chunkedData

    # for i in range(len(machineParts)):
    #     part = machineParts[i]
    #     if part in partsToSkip:
    #         continue
    #     if i == len(machineParts) - 1:
    #         chunkedData.append([part, sequence])
    #         break
    #     partSpace = part.count("#") + part.count("?")
    #     sequenceBroken = sequence[0]
    #     if partSpace < sequenceBroken:
    #         # remove eronius part
    #         chunkedData.append([part, []])
    #     else:
    #         # expand sequence
    #         j = 1
    #         # if k >= len(sequence):
    #         #     chunkedData.append([part, sequence])
    #         #     break
    #         nextSequenceBroken = sequenceBroken + sequence[j]
    #         while nextSequenceBroken + j + 1 <= partSpace:
    #             if j == len(sequence) - 1:
    #                 chunkedData.append(["".join(machineParts[i:]), sequence])
    #                 return chunkedData
    #             nextSequenceBroken = sequenceBroken + sequence[j]
    #             j += 1
    #         chunkedData.append([part, sequence[:j]])
    #         sequence = sequence[j:]
    return chunkedData


@functools.cache
def countValidPossibilities(part):
    # machines = eliminateUnknowns(part)
    # sequence = part[1]
    machines, sequence = part
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


def checkValidity(possibility, sequence):
    # if possibility.find("#" * (max(sequence) + 1)) != -1:
    #     return 0
    groups = list(filter(lambda x: x > 0, map(len, re.split("[.?]", possibility))))
    return groups == sequence


for i in range(len(data)):
    answer[data[i][0]] = []
    partitionedData = partition(*data[i])
    for part in partitionedData:
        print(part)
        partCount = countValidPossibilities(part)
        answer[data[i][0]].append((part[0], partCount))
    # print(answer)

grandTotal = 0
for line in answer:
    lineTotal = 1
    for part in answer[line]:
        lineTotal *= part[1]
    grandTotal += lineTotal
    print(line + ": " + str(lineTotal))
print("All possible arrangements: " + str(grandTotal))
