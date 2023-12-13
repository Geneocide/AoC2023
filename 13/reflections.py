from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

patterns = []
answers = []
with open(filepath, "r") as file:
    pattern = []
    for line in file:
        line = line.strip()
        if len(line) == 0:  # gap line
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)
    patterns.append(pattern)  # add last pattern


def checkIfMirrored(l1, l2):
    for i in range(min(len(l1), len(l2))):
        if l1[-(i + 1)] != l2[i]:
            return False
    return True


def handleRowMirrorFound(i):
    print("Mirror found at row index: " + str(i))
    answers.append(100 * i)


def handleColMirrorFound(i):
    print("Mirror found at col index: " + str(i))
    answers.append(i)


def columnize(pattern):
    return [list(x) for x in zip(*pattern)]


def lookForMirrors(pattern):
    rowCount = len(pattern)
    halfway = (int)(rowCount / 2) + 1
    for i in range(halfway, 0, -1):
        top = pattern[:i]
        bottom = pattern[i:]
        isMirrored = checkIfMirrored(top, bottom)
        if isMirrored:
            return i
        top = pattern[::-1][:i]
        bottom = pattern[::-1][i:]
        isMirrored = checkIfMirrored(top, bottom)
        if isMirrored:
            return rowCount - i
    return -1  # return -1 if no mirror found


for pattern in patterns:
    mirrorIndex = lookForMirrors(pattern)
    if mirrorIndex > 0:
        handleRowMirrorFound(mirrorIndex)
        continue
    columnizedPattern = columnize(pattern)
    mirrorIndex = lookForMirrors(columnizedPattern)
    if mirrorIndex > 0:
        handleColMirrorFound(mirrorIndex)

for answer in answers:
    print(answer)

print("Summerization: " + str(sum(answers)))  # answer 13828 (low), 29130
