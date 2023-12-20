# my solution relies on a bit of eye examinate of the input
# I worked backwards from rx, noticed only input was bb and that bb was Conjunction type
# and that all inputs into bb were also Conjunction, so I constructed this code to find when each input would be sending the high pulse and used LCM to extrapolate

from math import lcm
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


# gets all nodes that input into a conjunction. needed for initialization
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
bbInputs = {}
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
            if sender[1:] == "bb":
                for input in inputs:
                    bbInputs[input] = None


def pressButton(bbInputs):
    pulses = []
    # button sends low pulse to the broadcaster
    # print("button -low-> broadcaster")

    for output in network["broadcaster"][1]:
        pulses.append((output, 0, "broadcaster"))
        # print(f"broadcaster -low-> {output}")

    # pulses on one line are completed before next starts, process left to right within line
    while pulses:
        thisNode, pulseType, pulseFrom = pulses[0]
        pulses = pulses[1:]

        if thisNode in network:  # handles an output node the just absorbs pulses
            # direct approach like below is too slow
            # if thisNode == "rx" and pulseType == 0:
            #     return True
            newPulse = network[thisNode][0].getPulse(pulseType, pulseFrom)
            if newPulse is not None:
                for output in network[thisNode][1]:
                    pulses.append((output, newPulse, thisNode))
                    # print(
                    #     f"{thisNode} -{'low' if newPulse == 0 else 'high'}-> {output}"
                # if this is one of the inputs for rx and it's giving a high pulse, record presses to get there
                if thisNode in bbInputs and newPulse == 1:
                    bbInputs[thisNode] = buttonPresses
    return bbInputs


buttonPresses = 0
while any(v == None for v in bbInputs.values()):
    buttonPresses += 1
    bbInputs = pressButton(bbInputs)


# for node in network:
#     print(f"{node} - {network[node]}")

print(
    f"What is the fewest number of button presses required to deliver a single low pulse to the module named rx?"
)
print(f"Fewest button presses: {lcm(*bbInputs.values())}")  # answer 211712400442661
