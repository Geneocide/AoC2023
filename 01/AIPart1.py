def calculate_calibration_sum(file_path):
    total_sum = 0
    
    with open(file_path, 'r') as file:
        for line in file:
            # Remove newline characters
            line = line.strip()

            # Filter out non-digit characters and get the first and last digits
            digits = [int(char) for char in line if char.isdigit()]
            if digits:
                first_digit = digits[0]
                last_digit = digits[-1]

                # Combine and add to the total sum
                calibration_value = first_digit * 10 + last_digit
                total_sum += calibration_value

    return total_sum

# Provide the path to the input file
input_file_path = r'C:\Users\etreq\Advent of Code\2023\01\input.txt'

# Calculate and print the sum of all calibration values
sum_of_calibrations = calculate_calibration_sum(input_file_path)
print("The sum of all calibration values is:", sum_of_calibrations)