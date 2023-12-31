from pathlib import Path

filepath = Path(__file__).parent / "input.txt"
totalLowPulses = 0
totalHighPulses = 0
network = {}


class Flipflop(object):
    def __init__(self):
        self.isOn = False  # initiate off

    def getPulse(self, pulse, input):
        if pulse == 1:
            return  # ignore high pulses
        else:
            if self.isOn:
                self.isOn = False  # toggle on/off
                return 0  # send low pulse
            else:
                self.isOn = True  # toggle on/off
                return 1  # send high pulse


class Conjunction(object):
    def __init__(self, inputs):
        self.memory = {}
        for name in inputs:
            self.memory[name] = 0  # initiate to low

    def getPulse(self, pulse, input):
        self.memory[input] = pulse  # memory updated first upon getting a pulse
        if all(v == 1 for v in self.memory.values()):
            return 0  # send low if memory is all high
        return 1  # otherwise send high


def getConjunctionInputs(file, nodeName):
    inputs = []
    with open(filepath, "r") as file:
        for line in file:
            inputNode, sentTo = line.split(" -> ")
            if nodeName in sentTo:
                if inputNode[0] in ("%", "&"):
                    inputNode = inputNode[1:]
                inputs.append(inputNode)
    return inputs


# parse input
with open(filepath, "r") as file:
    for line in file:
        line = line.strip()
        sender, sentTo = line.split(" -> ")
        # broadcaster passes what it recieves to all its connections
        if sender[0] not in ("%", "&"):
            network[sender] = (None, sentTo.split(", "))
        # first character % indicates flip-flop module
        elif sender[0] == "%":
            network[sender[1:]] = (Flipflop(), sentTo.split(", "))
        # first character & indicates conjunction module
        elif sender[0] == "&":
            inputs = getConjunctionInputs(file, sender[1:])
            network[sender[1:]] = (Conjunction(inputs), sentTo.split(", "))


def pressButton():
    pressesLowPulses = 0
    pressesHighPulses = 0
    pulses = []
    # button sends low pulse to the broadcaster
    # print("button -low-> broadcaster")
    pressesLowPulses += 1

    for output in network["broadcaster"][1]:
        pulses.append((output, 0, "broadcaster"))
        # print(f"broadcaster -low-> {output}")
        pressesLowPulses += 1

    # pulses on one line are completed before next starts, process left to right within line
    while pulses:
        thisNode, pulseType, pulseFrom = pulses[0]
        pulses = pulses[1:]

        if thisNode in network:  # handles an output node the just absorbs pulses
            newPulse = network[thisNode][0].getPulse(pulseType, pulseFrom)
            if newPulse is not None:
                for output in network[thisNode][1]:
                    pulses.append((output, newPulse, thisNode))
                    # print(
                    #     f"{thisNode} -{'low' if newPulse == 0 else 'high'}-> {output}"
                    # )
                    if newPulse == 0:
                        pressesLowPulses += 1
                    else:
                        pressesHighPulses += 1
    return pressesLowPulses, pressesHighPulses


# button has been pressed 1000 times
for i in range(1000):
    pressesLowPulses, pressesHighPulses = pressButton()
    totalLowPulses += pressesLowPulses
    totalHighPulses += pressesHighPulses

# for node in network:
#     print(f"{node} - {network[node]}")

print(
    f"What do you get if you multiply the total number of low pulses sent by the total number of high pulses sent?"
)
print(
    f"Low pulse count: {totalLowPulses} * high pulse count: {totalHighPulses} = {totalLowPulses * totalHighPulses}"
)  # answer 889662720 (high), 883726240
# print(
#     f"For second example expecting 11687500 so off by {11687500 - totalLowPulses * totalHighPulses}"
# )
