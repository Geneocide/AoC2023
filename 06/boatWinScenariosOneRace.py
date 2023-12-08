import re
from pathlib import Path
filepath = Path(__file__).parent / "input.txt"

data = [] #going to be an array of time, record distance tuples

# limited solver for the quadradics in this porblem
def solveQuadradic(t, d):
    return (-1 * t + (t**2 - (4 * -1 * (-1 * d))) ** .5) // -2


with open(filepath, "r") as file:
    times = []
    distances = []
    for line in file:
        line = line.strip()
        if "Time" in line:
            times.append(int(re.sub("[^0-9]", "", line.split(':')[1])))
        if "Distance" in line:
            distances.append(int(re.sub("[^0-9]", "", line.split(':')[1])))
    for i in range(len(times)):
        data.append((times[i], distances[i]))

possibleVictories = []
for record in data:
    loseAt = solveQuadradic(record[0], record[1])
    possibleVictories.append(record[0] - 1 - (2 * loseAt)) #solved formula is floored so subtract double that amount from time to find possible millisecond holds that would lead to victory

finalProduct = 1
for victories in possibleVictories:
    finalProduct *= victories

print("Product of possible victories: " + str(finalProduct)) #answer 46561107