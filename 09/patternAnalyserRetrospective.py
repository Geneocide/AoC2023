# it occurs to me that the insert(0) could potentially be a source of unacceptable slowness due to having to increment all other list elements
# it wasn't a problem with this input, but an efficiency could be gained in this case by simply deleting all but the first element of the list once extrapolation is complete

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
        if all(point == 0 for point in differences):  # all 0 bottom list
            continue
        else:
            differencesBelow = differencesList[differencesList.index(differences) + 1]
            differences.insert(
                0, differences[0] - differencesBelow[0]
            )  # otherwise add extrapolated value to end of each differences list
    sequence.insert(
        0, sequence[0] - differencesList[0][0]
    )  # apply extrapolation to original sequence
    # final answer is the sum of the extrapolated element for all the initial series
    finalAnswer += sequence[0]

print("Sum of extrapolated values: " + str(finalAnswer))  # answer 988
