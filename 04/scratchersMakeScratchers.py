import re
from pathlib import Path
filepath = Path(__file__).parent / "input.txt"

with open(filepath, "r") as file:
    lines = [line.strip() for line in file]

class Card(object):
    id = 0 #not really used
    winningNumbers = []
    numbers = []
    copies = 1

    def __init__(self, id, winningNumbers, numbers):
        self.id = id
        self.winningNumbers = winningNumbers
        self.numbers = numbers

    def score(self, matches):
        for i in range(matches):
            cards[self.id + i].copies += 1 * self.copies #create a copy of next cards depending on matches and factoring in copies of this card

cards = []

for line in lines:
    cardNumberSplit = line.split(":")
    number = int(re.sub("[^0-9]", "", cardNumberSplit[0]))
    winningNumbersStr, cardNumbersStr = cardNumberSplit[1].split(" | ")
    winningNumbers = winningNumbersStr.split()
    cardNumbers = cardNumbersStr.split()
    card = Card(number, winningNumbers, cardNumbers)
    cards.append(card)

for card in cards:
    numberMatches = 0
    for number in card.numbers:
        if number in card.winningNumbers:
            numberMatches += 1
    card.score(numberMatches)

cardsTotal = 0
for card in cards:
    cardsTotal += card.copies

print("Cards Grand Total: " + str(cardsTotal)) #answer 14427616