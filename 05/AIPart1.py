# AI can't figure out how to parse the input
# I don't see anything of use here

def convert_number(source, destination, mapping):
    for dest_start, source_start, length in mapping:
        if source_start <= source < source_start + length:
            return dest_start + (source - source_start)
    return source

def find_lowest_location(seeds, maps):
    current_numbers = seeds.copy()
    
    for map_name, mapping in maps.items():
        next_numbers = []
        for number in current_numbers:
            converted_number = convert_number(number, number, mapping)
            next_numbers.append(converted_number)
        
        current_numbers = next_numbers
    
    return min(current_numbers)

def parse_input(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    seeds = list(map(int, lines[0].split()[1:]))
    maps = {}

    current_map = None
    for line in lines[1:]:
        if line.startswith("seed-to"):
            current_map = line.split()[1]
            maps[current_map] = []
        else:
            maps[current_map].append(list(map(int, line.split())))

    return seeds, maps

if __name__ == "__main__":
    input_file = "C:\Users\etreq\Advent of Code\2023\05\inputTest.txt"
    seeds, maps = parse_input(input_file)
    result = find_lowest_location(seeds, maps)
    print(f"The lowest location number is: {result}")
