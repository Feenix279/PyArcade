import analyzer
import funcs
import random

def result_counter(n):
    deck = funcs.generate_deck()
    results = [0,0,0,0,0,0,0,0,0,0]
    counter = 0
    for i in range(0,n):
        try:
            counter += 1
            random.shuffle(deck)
            hand = deck[:7]
            points = analyzer.analyze_hand(hand)
            if points == 814:
                results[-1] += 1
            else:
                index = funcs.convert_points_to_index(points)
                results[index] += 1
            if counter % 100000 == 0:
                print(f"Lebenszeichen: Counter = {counter}")
        except KeyboardInterrupt:
            break
    print(funcs.keys)
    print(results)
    print(f"Ergebnisse nach {counter} Versuchen: ")
    total_percentage = 0
    for key in funcs.keys:
        print(f"{key}: {results[funcs.keys.index(key)]}; {(results[funcs.keys.index(key)]/counter)*100}%")
        total_percentage += results[funcs.keys.index(key)]/counter*100

    print(f"Royal Flush: {results[-1]}; {results[-1]/counter}%")
    print(f"Gesamtprozente: {total_percentage}%")
    print("------------------------------")

if __name__ =="__main__":
    result_counter(int(input("Count: ")))