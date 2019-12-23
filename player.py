import pygame

class MOplayer():
    def __init__(self, name):
        self.hand = [] #array for player's hand
        self.name = name
        self.won = False  

    def draw(self, deck, x):
        for i in range(x):
            self.hand.append(deck.drawcard())
            #allows player draw multiple cards and appends them into hand array


    def showhand(self):
      print("{} Hand is: ".format(self.name))
      h=30
      for card in self.hand:
          print(card)
          displayimage(card.image,div_iwidth,div_iheight-h) #display's each card in a player's hand on to the game screen
          pygame.display.update()
          h=h+25 #moves each following card down by 25 to ensure the user can see all the cards
      
    def emptyhandcheck(self):
        if len(self.hand) == 0:
            self.won = True
            
    def discard(self):
      global down
      global skipturn
      global reverseturn
      if len(self.hand) != 0:
        discard_card = self.hand[down]
        self.throwAway(discard_card) #if the player has cards left in their hand, it will discard the card based on their keyboard input using throwAway
        
       
    def throwAway(self, discard):
       global maingamepile
       if len(maingamepile) > 1: #checks if there is a card or cards in play already
        lastcardplaced = maingamepile[-1] #if there is then the last card on the pile = the last card placed
        for card in self.hand:
            if card == discard: 
                if card.number == lastcardplaced.number or card.suit == lastcardplaced.suit: #checks if card selected to be discarded has the same suit or number as the last card in play on the pile
                    if card.number == "+2":
                        gametext_display("Computer Draws 2 more cards", 2, 4,15)
                        pygame.display.update()
                        Computer.draw(deck, 2) #if card is a +2, computer gets 2 more cards
                    elif card.number == "skip":
                        skipturn = True
                        gametext_display("Computer's Turn Will Be Skipped Next Round", 2, 4,15)
                        pygame.display.update() #if card is a skip, computer's turn will be skipped next in the main game loop
                    elif card.number == "reverse":
                        reverseturn = True
                        gametext_display("Computer's Turn Will Be Reversed Next Round", 2,4,15)
                        pygame.display.update() #if card is a reverse, computer's turn will be reversed next in the main game loop (effectively player gets another free turn)
                    self.hand.remove(card) #card is removed from player's hand
                    maingamepile.append(card) #card is added on to main game pile
                    break
                else:
                    invalidturn = True  
                    gametext_display("Invalid move. 1 card added to hand.",2,5,15)
                    pygame.display.update()
                    Player1.draw(deck, 1)
                    break  #if the user selects a card that isn't the same suit or number the card is invalidly played and they will face a draw card penalty
       else:
        for card in self.hand:
           if card == discard:
            self.hand.remove(card)
            maingamepile.append(card) #if there are no cards in play on the main game pile then the card the user selects will be discarded as normal (as this means the user is starting the game first)
    
