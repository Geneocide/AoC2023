# The AI fails to parse the input correctly. However, other than that it seems like it would succeed a brute force solve. Wouldn't work with the big numbers of part 2 though

# I asked it to be more efficient in the case of large numbers and it made up a formula for determing the that is totally made up. I'll include it below, but it's not referenced

def ways_to_beat_record(time, distance):
    ways = 0

    for hold_time in range(time):
        boat_speed = hold_time
        remaining_time = time - hold_time
        total_distance = boat_speed * remaining_time

        if total_distance > distance:
            ways += 1

    return ways

def efficient_ways_to_beat_record(time, distance):
    # Deriving a formula to calculate the number of ways efficiently
    max_hold_time = min(time - 1, distance)
    ways = max(0, max_hold_time * (max_hold_time + 1) // 2)

    return ways

def main():
    with open(r'C:\Users\etreq\Advent of Code\2023\06\inputTest.txt', 'r') as file:
        lines = file.readlines()

    total_ways = 1

    for line in lines:
        time, distance = map(int, line.split(':')[1].split())
        ways = ways_to_beat_record(time, distance)
        total_ways *= ways

    print("Total ways to beat the record:", total_ways)

if __name__ == "__main__":
    main()
