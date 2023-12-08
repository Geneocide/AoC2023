# I modified the code slightly to make it work. I added the split(':') to correctly get the numbers, and the AI had a else break in the points calculator that was causing any non-matching number to stop points counts.

def calculate_points(winning_numbers, your_numbers):
    points = 0
    for num in your_numbers:
        if num in winning_numbers:
            points += 1
            winning_numbers.remove(num)
    return 2 ** (points - 1) if points > 0 else 0

def main():
    with open(r'C:\Users\etreq\Advent of Code\2023\04\input.txt', 'r') as file:
        lines = file.readlines()

    total_points = 0

    for line in lines:
        # Split the line into winning numbers and your numbers
        winning_numbers, your_numbers = map(str.split, line.strip().split(':')[1].split('|'))
        
        # Convert the lists of numbers to sets
        winning_numbers = set(map(int, winning_numbers))
        your_numbers = set(map(int, your_numbers))
        
        # Calculate points for the current card and add to the total
        total_points += calculate_points(winning_numbers, your_numbers)

    print("Total points:", total_points)

if __name__ == "__main__":
    main()
