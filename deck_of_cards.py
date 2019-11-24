import random
import pygame

div_iwidth = 12
div_iheight = 12

class Card:
    def __init__(self, suit, number):
        self.suit = suit
        vals = {10: "reverse", 11:"skip", 12:"+2"}
        if int(number) < 10:
            self.number = int(number)
        else:
            self.number = vals[number]
        self.image = pygame.image.load(str(self) + ".png")

    def __eq__(self, other):
        if self.suit == other.suit and self.number == other.number:
            return True
        return False

    def __repr__(self):
        return self.showcard()

    def getImage():
        return self.image

    def showcard(self):
        return "{} {}".format(self.suit, self.number)

class Deck:
    def __init__(self):
        self.cards = []
        self.builddeck()

    def builddeck(self):
        for s in ["yellow","red","blue","green"]:
            for n in range(0,13):
                self.cards.append(Card(s, n))

    def showdeck(self):
        for card in self.cards:
            print(card)

    def shuffle(self):
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
      print("{} Hand is: ".format(self.name))
      for card in self.hand:
          print(card)
          #displayimage(cardImg,div_iwidth,div_iheight-2)

    def checkforuno(self):
        pass

    def showpile (self):
        print("'\nCards on the pile are")
        for card in self.pile:
            print(card)


    def discard(self): #remove random card - could be used in 'AI'
      while len(self.hand) != 0:
          discard_card = input("What card do you want to discard? ").split(" ")
          suit = discard_card[0]
          number = discard_card[1]
          int(number)
          discard = Card(suit, number)
          self.throwAway(discard)
          break

    def throwAway(self, discard):
       for card in self.hand:
          if card == discard:
              self.hand.remove(card)
              self.pile.append(card)



class AI(Player):
    def discard(self):
        ai_random_card = random.choice(self.hand)
        print("AI Random Choice: {}".format(ai_random_card))
        self.throwAway(ai_random_card)


deck = Deck()
#deck.builddeck()
#deck.showdeck()
deck.shuffle()
Player1 = Player('David')
AI = AI('AI')

Player1.draw(deck, 5)
AI.draw(deck, 5)
Player1.showhand()
AI.showhand()

Player1.discard()
Player1.showhand()

AI.discard()
AI.showhand()

#Player1.showpile()
