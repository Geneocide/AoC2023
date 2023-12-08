def is_possible(game_info, target_counts):
    for draw in game_info:
        draw_counts = {color: 0 for color in target_counts}
        for item in draw:
            parts = item.split()
            color = parts[1]
            count = int(parts[0])

            draw_counts[color] += count

            if draw_counts[color] > target_counts[color]:
                return False

    return True

def main():
    target_counts = {'red': 12, 'green': 13, 'blue': 14}
    possible_games = []

    with open(r'C:\Users\etreq\Advent of Code\2023\02\input.txt', 'r')  as file:
        for line in file:
            game_id, game_info = line.strip().split(':')
            game_info = [draw.strip().split(', ') for draw in game_info.split(';')]

            if is_possible(game_info, target_counts):
                possible_games.append(int(game_id.split()[1]))

    print("The sum of IDs of possible games is:", sum(possible_games))

if __name__ == "__main__":
    main()
