import re
from pathlib import Path
filepath = Path(__file__).parent / "input.txt"

# Read input from the file and strip out non-digits
with open(filepath, "r") as file:
    lines = [re.sub("[^0-9]", "", line.strip()) for line in file]

grandTotal = 0

# create each number from first and last digits and add to running total
for line in lines:
    first = line[0]
    last = line[-1]
    number = str.format(first) + str.format(last)
    grandTotal += int(number)

# Print the result
print("Grand Total: " + str(grandTotal)) #answer 54990