def compare_cards(card1, card2):
    order = "AKQJT98765432A"
    return order.index(card2) - order.index(card1)

def compare_hands(hand1, hand2):
    for c1, c2 in zip(hand1, hand2):
        comparison = compare_cards(c1, c2)
        if comparison != 0:
            return comparison
    return 0

def get_hand_rank(hand):
    hand_types = [
        ("AAAAA", 1),
        ("AAABB", 2),
        ("AAA22", 3),
        ("AAABC", 4),
        ("AABBC", 5),
        ("ABCDE", 6)
    ]

    for hand_type, rank in hand_types:
        if any(hand.count(card) != count for card, count in zip(hand_type, "54321")):
            continue
        return rank

def calculate_winnings(hands_and_bids):
    sorted_hands = sorted(hands_and_bids, key=lambda x: (get_hand_rank(x[0]), x[0]), reverse=True)
    
    total_winnings = sum(bid * (i + 1) for i, (_, bid) in enumerate(sorted_hands))
    
    return total_winnings

# Read input from input.txt
with open(r'C:\Users\etreq\Advent of Code\2023\07\inputTest.txt', 'r') as file:
    hands_and_bids = [line.strip().split() for line in file]

# Calculate and print the rank of each hand and total winnings
for hand, bid in hands_and_bids:
    rank = get_hand_rank(hand)
    print(f"{hand}: Rank {rank}")

total_winnings = calculate_winnings(hands_and_bids)
print(f"\nTotal Winnings: {total_winnings}")
