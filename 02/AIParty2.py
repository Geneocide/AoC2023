from itertools import product

def calculate_min_cubes(game):
    min_cubes = [float('inf')] * 3

    for subset in product(*game):
        min_cubes = [min(min_cubes[i], subset[i]) for i in range(3)]

    return min_cubes

def calculate_power(cubes):
    return cubes[0] * cubes[1] * cubes[2]

def main():
    with open(r'C:\Users\etreq\Advent of Code\2023\02\input.txt', 'r')  as file:
        input_data = file.readlines()

    total_power = 0
    game_data = []

    for line in input_data:
        if line.startswith("Game"):
            if game_data:
                game = []
                for subset_str in game_data:
                    cubes = [int(value.split()[0]) for value in subset_str.split(",")]
                    game.append(cubes)

                min_cubes = calculate_min_cubes(game)
                total_power += calculate_power(min_cubes)

                game_data = []  # Reset for the next game
        else:
            game_data.extend(line.strip().split(";"))

    # Process the last game if there is one
    if game_data:
        game = []
        for subset_str in game_data:
            cubes = [int(value.split()[0]) for value in subset_str.split(",")]
            game.append(cubes)

        min_cubes = calculate_min_cubes(game)
        total_power += calculate_power(min_cubes)

    print("The sum of the power of the minimum sets is:", total_power)

if __name__ == "__main__":
    main()
