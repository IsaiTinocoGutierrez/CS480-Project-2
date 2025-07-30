import random
from itertools import combinations

SUITS = ['s', 'h', 'd', 'c']  # spades, hearts, diamonds, clubs
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

def full_deck():
    return [rank + suit for rank in RANKS for suit in SUITS]

class Deck:
    def __init__(self):
        self.cards = full_deck()
        self.drawn = set()

    def draw(self, count=1):
        available = list(set(self.cards) - self.drawn)
        drawn_cards = random.sample(available, count)
        self.drawn.update(drawn_cards)
        return drawn_cards

    def mark_as_drawn(self, cards):
        self.drawn.update(cards)

    def reset(self):
        self.drawn.clear()
