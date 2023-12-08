def get_calibration_value(line):
    # Dictionary to map word representations of digits to actual digits
    word_to_digit = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }

    # Function to convert words to digits
    def convert_word_to_digit(word):
        return word_to_digit.get(word, ''.join(char for char in word if char.isdigit()))

    # Extract words from the line and convert them to digits
    digits = [convert_word_to_digit(word.lower()) for word in line.split() if word.isalpha() or any(char.isdigit() for char in word)]

    # If there's only one digit, use it as both the first and last digit
    if len(digits) == 1:
        digits.append(digits[0])

    # Combine the first and last digit to form a two-digit number
    calibration_value = int(digits[0] + digits[-1])

    return calibration_value

# Read input from the file
with open(r'C:\Users\etreq\Advent of Code\2023\01\input.txt', 'r') as file:
    lines = file.readlines()

# Calculate the sum of calibration values for all lines
total_calibration_sum = sum(get_calibration_value(line.strip()) for line in lines)

print(f"The sum of all calibration values is: {total_calibration_sum}")

