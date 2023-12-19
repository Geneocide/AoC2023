from pathlib import Path

filepath = Path(__file__).parent / "inputTest.txt"
blankLinePassed = False
workflows = {}
parts = []


with open(filepath, "r") as file:
    for line in file:
        # parsing rules because haven't gotten to blank line
        if not blankLinePassed:
            if line == "\n":
                blankLinePassed = True
                continue
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
        # parsing parts
        else:
            part = {}
            attributes = line.strip()[1:-1].split(",")
            for attribute in attributes:
                k, v = attribute.split("=")
                part[k] = int(v)
            parts.append(part)


def process(part, workflow):
    for step in workflow:
        if step[1]:
            condition = step[0]
            k = condition[0]
            if eval(f"{part[k]}{condition[1:]}") == True:
                return step[1]
        else:
            return step[0]


accepted = []
totalRatings = 0
line = ""
for part in parts:
    line += f"{str(part)}: in -> "
    workflowName = "in"
    while workflowName not in ("A", "R"):
        workflowName = process(part, workflows[workflowName])
        line += f"{workflowName} -> "
        if workflowName == "A":
            line = line[:-3]
            accepted.append(part)
            for attribute in part:
                totalRatings += part[attribute]
    print(line)
    line = ""

print(f"Total ratings of accepted parts: {totalRatings}")  # answer 398527
