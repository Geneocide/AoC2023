from functools import cmp_to_key
from pathlib import Path
filepath = Path(__file__).parent / "inputTest.txt"

def getUniqueCount(str):
    return len(set(str))

def getFrequencies(str):
    f = {}
    for char in str:
        f[char] = f.get(char, 0) + 1
    return f

# rank by first card, A high. Tie moves to next card
def compare(hand1, hand2):
    h1 = hand1[0]
    h2 = hand2[0]
    for i in range(len(h1)):
        c1 = h1[i]
        c2 = h2[i]
        if c1 == c2: #cards match, move to next card
            continue
        elif c1 > c2:
            return 1
        else: 
            return -1
    return 0 #hands match perfectly so order doesn't matter

# import and parse data
hands = []
typedHands = {}
rankedHands = {}
with open(filepath, "r") as file:
    for line in file:
        line = line.strip()
        hand, bid = line.split()
        cards = []
        for card in hand: #translate cards into numbers
            if card.isdigit():
                cards.append(int(card))
            else:
                if card == 'A':
                    cards.append(14)
                elif card == 'K':
                    cards.append(13)
                elif card == 'Q':
                    cards.append(12)
                elif card == 'J':
                    cards.append(11)
                elif card == 'T':
                    cards.append(10)
        hands.append((cards, int(bid)))
# sort by hand type

for i in range(7):
    typedHands[i] = []

# 5 of a kind > 4 of a kind > full house > three of a kind > two pair > pair > high card
# low numbers mean low rank
for hand in hands:
    uniqueCount = getUniqueCount(hand[0])
    if uniqueCount == 1: # then 5 of a kind
        typedHands[6].append(hand)
    elif uniqueCount == 2: # then 4 of a kind or full house
        frequencies = getFrequencies(hand[0])
        if 4 in frequencies.values(): # then 4 of a kind
            typedHands[5].append(hand)
        else: #then full house
            typedHands[4].append(hand)
    elif uniqueCount == 3: # then 3 of a kind or two pair
        frequencies = getFrequencies(hand[0])
        if 3 in frequencies.values(): # then 3 of a kind
            typedHands[3].append(hand)
        else: #then two pair
            typedHands[2].append(hand)
    elif uniqueCount == 4: # then pair
        typedHands[1].append(hand)
    else: # then high card
        typedHands[0].append(hand)

# sort within type by rank
for type in typedHands:
    hands = sorted(typedHands[type], key = cmp_to_key(compare))
    for hand in hands:
        rankedHands[len(rankedHands) + 1] = hand

winnings = 0
# calculate score = rank * bid
for rank in rankedHands:
    winnings += rank * rankedHands[rank][1]

print("Total winnings: " + str(winnings)) #answer 253201261 (low), 253205868