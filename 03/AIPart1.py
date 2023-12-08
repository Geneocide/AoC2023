def is_valid_char(char):
    return char.isdigit() or char == '.'


def get_adjacent_numbers(grid, row, col):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]
    adjacent_numbers = []

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        while 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and is_valid_char(grid[new_row][new_col]):
            if grid[new_row][new_col].isdigit():
                adjacent_numbers.append(int(grid[new_row][new_col]))
            new_row, new_col = new_row + dr, new_col + dc

    return adjacent_numbers


def calculate_part_numbers_sum(grid):
    part_numbers_sum = 0

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if is_valid_char(grid[row][col]):
                part_numbers_sum += sum(get_adjacent_numbers(grid, row, col))

    return part_numbers_sum


def main():
    with open(r'C:\Users\etreq\Advent of Code\2023\03\input.txt', 'r') as file:
        engine_schematic = [line.strip() for line in file]

    part_numbers_sum = calculate_part_numbers_sum(engine_schematic)

    print("Sum of part numbers:", part_numbers_sum)


if __name__ == "__main__":
    main()
