from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

sequences = []

#parse input. each line is a series.
with open(filepath, "r") as file:
    for line in file:
        sequences.append(line.strip().split())

#need to consider lists of list or something
differencesList = [[]]
for sequence in sequences:
    while len(differencesList) == 0 or all(point == 0 for point in differencesList[-1]):
        differencesList.append(list(map(lambda i, j: i - j, sequences)))
    
#determine pattern by
#1) create a list of differences for each element in series
#2) repeat until all differences are 0
#3) starting with the all 0 list, extrapolate the next value. in the case of the 0's it will always be a 0

#final answer is the sum of the extrapolated element for all the initial series