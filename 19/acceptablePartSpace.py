from heapq import heappop, heappush
from pathlib import Path

filepath = Path(__file__).parent / "input.txt"
blankLinePassed = False
workflows = {}
part = {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)}
parts = []
queue = [("in", part)]
totalSize = 0

with open(filepath, "r") as file:
    for line in file:
        # parsing rules because haven't gotten to blank line
        if not blankLinePassed:
            if line == "\n":
                break
            line = line.strip()
            openBracketIndex = line.index("{")
            workflowName, workflowRules = (
                line[:openBracketIndex],
                line[openBracketIndex + 1 : -1],
            )
            workflows[workflowName] = []
            for rule in workflowRules.split(","):
                if ":" in rule:
                    sendTo, condition = rule.split(":")
                else:
                    sendTo = rule
                    condition = None
                workflows[workflowName].append((sendTo, condition))


def sizePart(part):
    size = 1
    for v in part:
        size *= part[v][1] - part[v][0] + 1
    return size


def modifyPart(condition, part):
    oPart = part.copy()
    if condition:
        v = condition[0]
        if condition[1] == "<":
            part[v] = (part[v][0], int(condition[2:]) - 1)
            oPart[v] = (int(condition[2:]), oPart[v][1])
        else:
            part[v] = (int(condition[2:]) + 1, part[v][1])
            oPart[v] = (oPart[v][0], int(condition[2:]))
    return part, oPart


while queue:
    workflowName, part = heappop(queue)
    print(f"{workflowName}: {part}")
    for rule in workflows[workflowName]:
        if rule[1]:
            sendTo = rule[1]
            condition = rule[0]
            meetsConditionPart, part = modifyPart(condition, part)
            if sendTo in ("A", "R"):
                if sendTo == "A":
                    parts.append(meetsConditionPart.copy())
            else:
                heappush(queue, (sendTo, meetsConditionPart.copy()))
        else:
            sendTo = rule[0]
            if sendTo in ("A", "R"):
                if sendTo == "A":
                    parts.append(part.copy())
            else:
                heappush(queue, (sendTo, part.copy()))
for part in parts:
    size = sizePart(part)
    totalSize += size
    print(f"{part} - {size}")

print(f"Distinct acceptable part ratings: {totalSize}")  # answer 133973513090020
