import analyzer
import funcs
import random
import matplotlib



def result_counter(n):
    deck = funcs.generate_deck()
    counter = 0
    for i in range(0,n):
        try:
            counter += 1
            random.shuffle(deck)
            hand = deck[:7]
            points = analyzer.analyze_hand(hand)
            if counter % 100000 == 0:
                print(f"Lebenszeichen: Counter = {counter}")
        except KeyboardInterrupt:
            break