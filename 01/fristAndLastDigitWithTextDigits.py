# I had the idea later to reverse the string and reverse the number words, might have saved some pain... like look for xis when finding the last digit

import re
from pathlib import Path
filepath = Path(__file__).parent / "input.txt"

# Read input from the file, replace text digits with regular digits and strip out non-digts
with open(filepath, "r") as file:
    lines = []
    for line in file:
        line = line.strip()
        first = last = None
        for i in range(len(line)): #find first digit
            if(line[i].isdigit()): #found a normal digit, stop looking
                first = line[i]
                break
            if(re.search("one|two|three|four|five|six|seven|eight|nine", line[:i+1]) != None): #found a word digit
                first = line[:i+1].replace("one", "1").replace("eight", "8").replace("two", "2").replace("three", "3").replace("four", "4").replace("five", "5").replace("six", "6").replace("seven", "7").replace("nine", "9") #replacing front to back requires eight before two
                break
        for i in range(1, len(line) + 1): #find last digit
            if(line[-i].isdigit()): #found a normal digit, stop looking
                last = line[-i]
                break
            if(re.search("one|two|three|four|five|six|seven|eight|nine", line[-i:]) != None): #found a word digit
                last = line[-i:].replace("eight", "8").replace("five", "5").replace("one", "1").replace("two", "2").replace("three", "3").replace("four", "4").replace("six", "6").replace("nine", "9") .replace("seven", "7")          
                break
        lines.append(re.sub("[^0-9]", "", (str(first) + str(last))))
            


#with open(filepath, "r") as file:
#    lines = [re.sub("[^0-9]", "", line.strip().replace("one", "1").replace("eight", "8").replace("two", "2").replace("three", "3").replace("four", "4").replace("five", "5").replace("six", "6").replace("seven", "7").replace("nine", "9")) for line in file]

grandTotal = 0

# create each number from first and last digits and add to running total
for line in lines:
    grandTotal += int(line)

# Print the result
print("Grand Total: " + str(grandTotal)) #answer 53794, 54394, 54640, 54623, 54473