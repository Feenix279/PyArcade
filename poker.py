import random
vals = ["Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King"]
suits = ["Spades", "Hearts", "Diamonds", "Clubs"]

class card():
    def __init__(self, value, suit):
        self.name = value
        self.order = vals.index(value)
        self.suit = suit
    def stringify(self):
        return str(self.value+ " of "+self.suit+ " ")
    
def generate_deck():
    deck = []
    for val in vals:
        for suit in suits:
            deck.append(card(value=val, suit=suit))
    random.shuffle(deck)
    return deck
def check_multiples(cards:list[card]):
    for val in vals:
        pass
def get_hand(community:list[card], hole:list[card]):
    cards = community + hole
    print(is_flush(cards))
    
def is_flush(cards:list[card]):
    flush = False
    for suit in suits:
        count = 0
        for card in cards:
            if card.suit == suit:
                count += 1
        if count >= 5:
            flush = True
    return flush

def is_straight(cards:list[card]):
    pass
    
def testfuncs():
    #flushtest
    flushcount = 0
    for i in range(0,100000000):
        deck = generate_deck()
        if is_flush(deck[:5] + deck[-2:]):
            flushcount += 1
        #print(len(deck[:5] + deck[-2:]))
    print(f"Flushcount = {flushcount}")
if __name__ =="__main__":
    testfuncs()
        
    