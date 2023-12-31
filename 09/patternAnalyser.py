# learned from AI that could switch the all() checks to any() and it's cleaner. any returns false if all 0.

from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

sequences = []
finalAnswer = 0

# parse input. each line is a series.
with open(filepath, "r") as file:
    for line in file:
        sequences.append(list(map(int, line.strip().split())))


# determine pattern
for sequence in sequences:
    differencesList = []
    while len(differencesList) == 0 or not all(
        point == 0 for point in differencesList[-1]
    ):  # repeat until all differences are 0
        # create a list of differences for each element in series
        if len(differencesList) == 0:
            differencesList.append(
                list(
                    map(
                        lambda i: sequence[i + 1] - sequence[i],
                        range(len(sequence) - 1),
                    )
                )
            )
        else:
            differencesList.append(
                list(
                    map(
                        lambda i: differencesList[-1][i + 1] - differencesList[-1][i],
                        range(len(differencesList[-1]) - 1),
                    )
                )
            )
    for differences in reversed(differencesList):
        if not all(point == 0 for point in differences):  # all 0 bottom list
            continue
        else:
            differencesBelow = differencesList[differencesList.index(differences) + 1]
            differences.append(
                differences[-1] + differencesBelow[-1]
            )  # otherwise add extrapolated value to end of each differences list
    sequence.append(
        sequence[-1] + differencesList[0][-1]
    )  # apply extrapolation to original sequence
    # final answer is the sum of the extrapolated element for all the initial series
    finalAnswer += sequence[-1]

print("Sum of extrapolated values: " + str(finalAnswer))  # answer 1995001648
