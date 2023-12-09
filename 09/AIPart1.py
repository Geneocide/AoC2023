#bard couldn't take the input even though I shortened it
#chatgpt isn't getting it right, it's not actually doing the extrapolation part, just the difference part

def extrapolate_next_value(history):
    while any(history):
        history = [history[i + 1] - history[i] for i in range(len(history) - 1)]
    return history[0]

def main():
    with open(r"C:\Users\etreq\Advent of Code\2023\09\inputTest.txt", "r") as file:
        reports = [list(map(int, line.split())) for line in file.readlines()]

    extrapolated_values = [extrapolate_next_value(report) for report in reports]

    sum_of_extrapolated_values = sum(extrapolated_values)

    print("Sum of extrapolated values:", sum_of_extrapolated_values)

if __name__ == "__main__":
    main()
