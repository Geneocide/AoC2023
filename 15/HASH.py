from pathlib import Path

filepath = Path(__file__).parent / "input.txt"

strings = []
with open(filepath, "r") as file:
    for line in file:
        strings = line.strip().split(",")

results = 0
for string in strings:
    v = 0
    for char in string:
        v += ord(char)
        v *= 17
        v %= 256
    results += v
    # print(string + ": " + str(v))

print("Sum of results: " + str(results))  # answer 512797
