import analyzer
import funcs
import random

def random_takes():
    deck = funcs.generate_deck()
    counter = 0
    while True:
        try:
            counter += 1
            random.shuffle(deck)
            hand = deck[:7]
            points = analyzer.analyze_hand(hand)
            if counter % 100000 == 0:
                print(f"Lebenszeichen: Counter = {counter}")
            if points == 814:
                print(hand)
                print(points, f"Try {counter}")
                input("Weiter ")
        except KeyboardInterrupt:
            break
def check_all():
    deck = funcs.generate_deck()
    counter = 0
    keys = funcs.keys
    while keys:
        try:
            counter += 1
            random.shuffle(deck)
            hand = deck[:7]
            points = round(analyzer.analyze_hand(hand))
            ind = int(round(points/1000, 0))
            res = funcs.keys[ind]
            if res in keys:
                print(f"{res} funktioniert, erreichter Wert: {points} mit Hand {hand}")
                keys.remove(res)
            if counter % 100000 == 0:
                print(f"Lebenszeichen: Counter = {counter}")

        except KeyboardInterrupt:
            break
def straight_flush():
    deck = []
    for value in analyzer.vals:
        deck.append([value, "Spades"])
    print(analyzer.analyze_hand(deck))
    print(deck[:7])
if __name__ == "__main__":
    #straight_flush()
    #random_takes()
    check_all()