import analyzer
import random

keys = ["High Card", "Pair", "Two Pair", "Triplet", "Straight", "Flush","Full House","Four of a kind", "Straight Flush"]

def generate_deck():
    deck = []
    for suit in analyzer.suits:
        for value in analyzer.vals:
            deck.append([value,suit])
    random.shuffle(deck)
    return deck