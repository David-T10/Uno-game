import random
import pygame
from sql_database import login

pygame.init() #initialises pygame
width = 800
height = 600
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
mouseposition = pygame.mouse.get_pos()
uno_window = pygame.display.set_mode((width, height)) #creates a window with specified resolution (x,y)
pygame.display.set_caption('Python UNO') #sets window title
fps = pygame.time.Clock() #creates a clock that counts fps
fps.tick(60)
def text_objects(text, font, colour): #this function takes the rectangle and puts it over the whole of the text so it can be moved as one
    textSurface = font.render(text, True, colour) 
    return textSurface, textSurface.get_rect()

def createbutton(button_name,width1,height2,w1,h2,colour):
    mouse = pygame.mouse.get_pos()
    button_font_size = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(button_name, button_font_size, colour)
    textRect.center = ( (width1+(w1/2)), (height2+(h2/2)) )
    uno_window.blit(textSurf, textRect)

def startup_menu():
    startup = True
    while startup:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        uno_window.fill(white)
        titlefont = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects('Welcome to UNO', titlefont, black) #referencing the surface and box around the text so it can be moved around
        TextRect.center = ((width/2) ,(height/2))
        uno_window.blit(TextSurf, TextRect)
        createbutton('SINGLEPLAYER',150,450,100,50,green)
        createbutton('MULTILPLAYER',370,450,100,50,blue)
        createbutton('QUIT',550,450,100,50,red)
        pygame.display.update()
    

pile = []
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
        self.builddeck()
        
    def builddeck(self):
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
    def __init__(self, u_name_l):
        self.hand = []
        self.pile = []
        self.name = u_name_l

    def draw(self, deck, x):
        for i in range(x):
            self.hand.append(deck.drawcard())
            #return self #allows player draw multiple cards
            
    
    def showhand(self):
      print("Your hand is")
      for card in self.hand:
          card.showcard()

    def discard(self): #remove random card - could be used in 'AI'
      discard_card = input("What card do you want to discard? ")
      if discard_card in self.hand:
        self.hand.remove(discard_card)
        self.pile.append(discard_card)
        return self.pile

def game():
    startup_menu()
    deck = Deck()
    deck.shuffle()
    #deck.showdeck()
    Player1 = Player(login)
    Player1.draw(deck, 5)
    Player1.showhand()
    Player1.discard()
    Player1.showhand()

game()
    


