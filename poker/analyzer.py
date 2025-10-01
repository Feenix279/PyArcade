vals = ["2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace"]
suits = ["Spades", "Hearts", "Diamonds", "Clubs"]

def analyze_hand(cards:list[list]):
    maxval = 0
    checks = [check_high_card, check_multiples, check_straight, check_straight_flush]
    for check in checks:
        val = check(cards)
        if val>maxval:
            maxval = val
    return maxval

def check_high_card(cards:list[list])->int:
    """definiton of card: [value, suit]"""
    maxval = 0
    for card in cards:
        if vals.index(card[0])+2>maxval:
            maxval = vals.index(card[0])+2
    return 00+maxval

def check_straight_flush(cards:list[list])->int:
    """definiton of card: [value, suit]"""
    suitcounts = [0,0,0,0]
    for card in cards:
        suitcounts[suits.index(card[1])] += 1
    for i in suitcounts:
        if i >= 5:
            working = [card for card in cards if card[1] == suits[suitcounts.index(i)]]

            straight = check_straight(working)
            if straight > 400:
                return 400+straight
            
            return 500+check_high_card(working)
    return 0
        
def check_straight(cards:list[list])->int:
    """definiton of card: [value, suit]"""
    maxval = 0
    values = []
    for card in cards:
        values.append(card[0])

    for card in cards:
        straight = True
        for i in range(1,5):
            try:
                if not vals[vals.index(card[0])-i] in values or vals.index(card[0])-i < -1:
                    straight = False

            except IndexError:
                straight = False
        if straight:
            maxval = 400+vals.index(card[0])+2
    return maxval

def check_multiples(cards:list[list])->int:
    """definiton of card: [value, suit]"""
    multiples = [0,0,0,0,0,0,0,0,0,0,0,0,0]
    maxval = 0

    def update_maxval(val, maxval):
        if val>maxval:
            maxval = val
        return maxval

    for card in cards:
        multiples[vals.index(card[0])] += 1
    
    pair = False
    triplet = False
    ind = 1
    for multiple in multiples:
        ind += 1
        if multiple == 2:
            if pair:
                maxval = update_maxval(200+ind,maxval)
            if triplet:
                maxval = update_maxval(600+multiples.index(3)+2,maxval)
            pair = True
            maxval = update_maxval(100+ind,maxval)
        elif multiple == 3:
            if pair:
                maxval = update_maxval(600+ind,maxval)
            triplet = True
            maxval = update_maxval(300+ind,maxval)
        elif multiple == 4:
            maxval = update_maxval(700+ind,maxval)
    return maxval
