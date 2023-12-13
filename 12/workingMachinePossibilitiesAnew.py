from itertools import combinations
import re
from pathlib import Path

filepath = Path(__file__).parent / "inputTest.txt"

data = {}
answer = {}

with open(filepath, "r") as file:
    for line in file:
        m, s = line.strip().split()
        mu = m
        su = s
        # for i in range(4):
        #     mu += "?" + m
        #     su += "," + s
        sequenceList = list(map(int, su.split(",")))
        data[len(data)] = (mu, sequenceList)


def partition(machines, sequence):
    # too complex to chunk
    if max(sequence) > 3:
        return [[machines, sequence]]
    machines = re.sub(r"\.\.+", ".", machines.strip("."))
    machineParts = re.split("[.]", machines)
    chunkedData = []
    partsToSkip = []

    for i in range(len(machineParts)):
        part = machineParts[i]
        if part in partsToSkip:
            continue
        if i == len(machineParts) - 1:
            chunkedData.append([part, sequence])
            break
        partSpace = part.count("#") + part.count("?")
        sequenceBroken = sequence[0]
        if partSpace < sequenceBroken:
            # remove eronius part
            chunkedData.append([part, []])
        else:
            # expand sequence
            j = 1
            # if k >= len(sequence):
            #     chunkedData.append([part, sequence])
            #     break
            nextSequenceBroken = sequenceBroken + sequence[j]
            while nextSequenceBroken + j + 1 <= partSpace:
                if j == len(sequence) - 1:
                    chunkedData.append(["".join(machineParts[i:]), sequence])
                    return chunkedData
                nextSequenceBroken = sequenceBroken + sequence[j]
                j += 1
            chunkedData.append([part, sequence[:j]])
            sequence = sequence[j:]
    return chunkedData

    for part in machineParts:
        chunkedData.append([part, []])
        # if last part return all that's left
        if part == machineParts[-1]:
            chunkedData[-1][-1] = sequence
            break
        partSpace = part.count("#") + part.count("?")
        for j in range(len(sequence)):
            sequenceBroken = sum(sequence[: j + 1])
            # if there aren't enough slots to fill the sequence requirements
            if sequenceBroken >= partSpace:
                sequence = sequence[j:]
                break
            chunkedData[-1][-1].append(sequence[j])
    if chunkedData == []:  # failed to chunk
        return [[machines, sequence]]
    return chunkedData


# def partition(machines, sequence):
#     machines = re.sub(r"\.\.+", ".", machines.strip("."))
#     countOfMachinesBetweenKnownWorking = list(
#         filter(lambda x: x > 0, map(len, re.split("[.]", machines)))
#     )
#     chunkedData = []
#     for x in countOfMachinesBetweenKnownWorking:
#         sequenceTotal = 0
#         for i in range(len(sequence)):
#             if x < sequence[i]:
#                 if machines[:x].count("?") < sequence[i]:
#                     chunkedData.append((machines[:x], [0]))
#                     machines = machines[(x + 1) :]
#                     break
#             sequenceTotal += sequence[i]
#             if sequenceTotal >= x:
#                 chunkedData.append((machines[:x], sequence[: (max(1, i))]))
#                 machines = machines[(x + 1) :]
#                 sequence = sequence[(max(1, i)) :]
#                 break
#         if len(sequence) > 0:
#             chunkedData.append((machines, sequence))
#     if chunkedData == []:  # failed to chunk
#         return [(machines, sequence)]
#     return chunkedData


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
