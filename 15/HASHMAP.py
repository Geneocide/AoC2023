import re
from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

strings = []
with open(filepath, "r") as file:
    for line in file:
        strings = line.strip().split(",")


def getOperatorIndex(s):
    try:
        return s.index("-")
    except:
        return s.index("=")


def hash(s):
    v = 0
    for c in s:
        v += ord(c)
        v *= 17
        v %= 256
    return v


def prettyPrint():
    for boxNumber in boxes:
        printLine = ""
        if len(boxes[boxNumber]) == 0:
            continue
        printLine += "Box " + str(boxNumber) + ": "
        for lense in boxes[boxNumber]:
            printLine += "[" + lense + " " + str(boxes[boxNumber][lense]) + "] "
        print(printLine)
    print("\n")


# build 255 boxes required
boxes = {}
for i in range(256):
    boxes[i] = {}

# parse instructions for moving lenses
for string in strings:
    operatorIndex = getOperatorIndex(string)
    label = string[:operatorIndex]
    boxNumber = hash(label)
    box = boxes[boxNumber]
    operator = string[operatorIndex]
    if operator == "-":
        # remove labelled lense
        boxes[boxNumber] = {
            key: value for key, value in boxes[boxNumber].items() if key != label
        }
    if operator == "=":
        value = int(string[operatorIndex + 1 :])
        box[label] = value
    # print("After " + string)
    # prettyPrint()

# calculate focusing power
focalPowerTotal = 0
for boxNumber in boxes:
    box = boxes[boxNumber]
    for lenseLabel in box:
        focalPower = 0
        focalLength = box[lenseLabel]
        lenseSlot = (
            list(box.keys()).index(lenseLabel) + 1
        )  # plus one because base 1 in example
        focalPower = (boxNumber + 1) * (lenseSlot) * focalLength
        # print(lenseLabel + " = " + str(focalPower))
        focalPowerTotal += focalPower
print("Total focal power: " + str(focalPowerTotal))  # answer 262454
