# I had to make the same adjustments as for Part 1 and more. It wasn't factoring in duplicate cards as it went, and it was calculating matches wrong.


def calculate_points(winning_numbers, your_numbers):
    points = 0
    for num in your_numbers:
        if num in winning_numbers:
            points += 1
            winning_numbers.remove(num)
    return points


def process_cards(cards):
    total_cards = [1] * len(cards)
    for i in range(len(cards)):
        card = cards[i]
        matching_numbers = calculate_points(card[0], card[1])
        for j in range(i + 1, min(i + matching_numbers + 1, len(cards))):
            total_cards[j] += 1 * total_cards[i]
    return total_cards


def main():
    with open(r"C:\Users\etreq\Advent of Code\2023\04\input.txt", "r") as file:
        lines = file.readlines()

    cards = []

    for line in lines:
        # Split the line into winning numbers and your numbers
        winning_numbers, your_numbers = map(
            str.split, line.strip().split(":")[1].split("|")
        )

        # Convert the lists of numbers to sets
        winning_numbers = list(map(int, winning_numbers))
        your_numbers = list(map(int, your_numbers))

        # Add the card to the list
        cards.append((winning_numbers, your_numbers))

    total_cards = process_cards(cards)

    # Sum the total number of scratchcards
    total_scratchcards = sum(total_cards)

    print("Total scratchcards:", total_scratchcards)


if __name__ == "__main__":
    main()
