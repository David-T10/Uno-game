import random

class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def __unicode__(self):
        return self.showcard()
    def __str__(self):
        return self.showcard()
    def __repr__(self):
        return self.showcard()

    def showcard(self):
        if self.number == 10:
            number = "Reverse"
        elif self.number == 11:
            number = "Skip"
        elif self.number == 12:
            number = "+2"
        else:
            number = self.number
            
        print ("{} {}".format(self.suit, number))
        
class Deck:
    def __init__(self):
        self.cards = []
        self.build()
        
    def build(self):
        for s in ["Yellow","Red","Blue","Green"]:
            for n in range (0,13):
                self.cards.append(Card(s, n))
                
                
    def showdeck(self):
        for card in self.cards:
            card.showcard()

    def shuffle(self):
        for i in range(len(self.cards)-1, 0, -1):
            random.shuffle(self.cards)

    def drawcard(self):
        return self.cards.pop()

    def discard(self):
        return self.hand.pop()

class Player:
    def __init__(self, name):
        self.hand = []
        self.pile = []
        self.name = name
        hand = self.hand

    def draw(self, deck):
        self.hand.append(deck.drawcard())
        return self #allows player draw multiple cards

    def showhand(self):
        for card in self.hand:
            card.showcard()
    
    def place(self, hand):
        self.pile.append(hand.discard())
        return self

    '''def showpile(self):
        for card in self.pile:
           card.showcard()'''
        
        
        
        
      
#card = Card("Yellow",6)
#card.showcard()


deck = Deck()
deck.shuffle()
deck.showdeck()
#deck.showdeck()
David = Player("David")
#David.draw(deck).draw(deck)
David.place(David.hand)
David.showhand()


