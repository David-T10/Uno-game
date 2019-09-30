
import random

class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def __unicode__(self):
        return self.showcard()

    def __eq__(self, other):
        if self.suit == other.suit and self.number == other.number:
            return True
        return False
    
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
            
        print("{} {}".format(self.suit, number))
        
class Deck:
    def __init__(self):
        self.cards = []

        self.builddeck()
        
    def builddeck(self):
        for s in ["Yellow","Red","Blue","Green"]:
            for n in range(0,13):
                self.cards.append(Card(s, n))
                
    def showdeck(self):
        for card in self.cards:
            card.showcard()

    def shuffle(self):
        for i in range(len(self.cards) - 1, 0, -1):
            random.shuffle(self.cards)

    def drawcard(self):
        return self.cards.pop()

    def discard(self):
        return self.hand.pop()
    

class Player:
    def __init__(self, u_name_l):
        self.hand = []
        self.pile = []
        self.name = u_name_l

    def draw(self, deck, x):
        for i in range(x):
            self.hand.append(deck.drawcard())
            #return self #allows player draw multiple cards
            
    
    def showhand(self):
      print("\nYour hand is")
      for card in self.hand:
          card.showcard()

    def showpile (self):
        print("'\nCards on the pile are")
        for card in self.pile:
            card.showcard()
          

    def discard(self): #remove random card - could be used in 'AI'
      discard_card = input("What card do you want to discard? ").split(' ')
      suit = discard_card[0]
      number = int(discard_card[1])
      discard_card = Card(suit, number)
      if discard_card in self.hand:
        self.hand.remove(discard_card)
        self.pile.append(discard_card)
        
#def add_player():   
      #pile.append(discarded_card)

    
    #def place(self, hand):
     #   self.pile.append(hand.discard'''change this to a pop method'''())
      #  return self

        
        
        
        
      
#card = Card("Yellow",6)
#card.showcard()

deck = Deck()
deck.shuffle()
#deck.showdeck()
Player1 = Player('David')
Player1.draw(deck, 5)
Player1.showhand()
Player1.discard()
Player1.showhand()
Player1.showpile()

#David.draw(deck).draw(deck)
#David.place(David.hand)
#David.showhand()


