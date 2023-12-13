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


def checkForSmudge(r1, r2):
    b1 = list(map(lambda c: 1 if c == "#" else 0, r1))
    b2 = list(map(lambda c: 1 if c == "#" else 0, r2))
    xored = [a ^ b for a, b in zip(b1, b2)]
    if xored.count(1) == 1:
        # smudge found
        return True
    return False


def checkIfMirrored(l1, l2):
    smudgeFound = False
    for i in range(min(len(l1), len(l2))):
        if l1[-(i + 1)] != l2[i]:
            if not smudgeFound:  # if a smudge hasn't already been found
                smudgeFound = checkForSmudge(l1[-(i + 1)], l2[i])  # look for smudge
                if smudgeFound:  # if exactly 1 smudge found
                    continue  # keep checking
            return False  # otherwise stop looking as usual
    return smudgeFound  # don't count a mirror without a smudge


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
    for i in range(1, len(pattern)):
        top = pattern[:i]
        bottom = pattern[i:]
        isMirrored = checkIfMirrored(top, bottom)
        if isMirrored:
            return i
        # top = pattern[::-1][:i]
        # bottom = pattern[::-1][i:]
        # isMirrored = checkIfMirrored(top, bottom)
        # if isMirrored:
        #     return rowCount - i
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
    else:
        print("NO MIRROR FOUND")

for answer in answers:
    print(answer)

print(
    "Summerization: " + str(sum(answers))
)  # answer 42861 (high), 12082 (low), 32796 (low), 33438
