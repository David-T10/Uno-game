import random
import pygame
import os
import time  
from sys import exit

pygame.init() #initialises pygame
x = 800
y = 600
div_iwidth = 750
div_iheight = 550
transparent = (0,0,0,0)
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
orange = (255,165,0)
mouseposition = pygame.mouse.get_pos()

def displayimage(image_name,div_iwidth, div_iheight):
    iwidth = x-div_iwidth
    iheight = y-div_iheight
    uno_window.blit(image_name, (iwidth,iheight))
    pygame.display.update()
    time.sleep(0.3)


class Card:
    def __init__(self, suit, number):
        #doesn't work if i enter a number in the vals dictionary (need to be fixed)
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
      h=30
      for card in self.hand:
          print(card)
          displayimage(card.image,div_iwidth,div_iheight-h)
          h=h+25

    def showpile (self):
        print("'\nCards on the pile are")
        for card in self.pile:
            print(card)


    def discard(self): 
      if len(self.hand) != 0:
          discard_card = input("What card do you want to discard? ").split(" ")
          suit = discard_card[0]
          number = discard_card[1]
          int(number)
          discard = Card(suit, number)
          self.throwAway(discard)
      elif len(self.hand) == 2:
          check_if_uno_called()
      elif len(self.hand) == 1:
        add_screen()
        gametext_display("Player1 won. Game Over", 2, 2, 40)
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        exit()
          

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
        if len(self.hand) == 0:
            add_screen()
            gametext_display("Computer won. Game Over", 2, 2, 20)
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
            exit()

    def showhand(self):
        print("{}'s Hand is: ".format(self.name))
        h=30
        for card in self.hand:
            print(card)
            displayimage(card.image,div_iwidth-600,div_iheight-h)
            h=h+25

Player1 = Player('Player1')
Computer = AI('Computer')

#GUI + EXTRA FUNCTION STUFF

def text_objects(text, font): #this function takes the rectangle and puts it over the whole of the text so it can be moved as one
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def gametext_display(text,divby_x,divby_y,fontsize):
    gametext = pygame.font.Font('freesansbold.ttf', fontsize)
    TextSurf,TextRect = text_objects(text, gametext)
    TextRect.center = ((x/divby_x) ,(y/divby_y))
    uno_window.blit(TextSurf, TextRect)

def deal_deck_selected():
        deck = Deck()
        deck.shuffle()
        Player1.draw(deck, 4)
        Player1.showhand()
        Computer.draw(deck, 4)
        Computer.showhand()
        gametext_display('Player1 starts first, press SPACE to discard a card',2,12,15)
        pygame.display.update()
        

def check_if_uno_called():
    time_left = True
    countdown = True
    while time_left == True and countdown == True:
        gametext_display('Press U to call UNO, you have 5 seconds', 2, 1.2, 15)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_u:
                    countdown = False
                    break
                
                
         


def discard_card_selected():
    Player1.discard()
    Computer.discard()
    empty_singleplayer_screen()
    Player1.showhand()
    Computer.showhand()
    

def deck_image(width,height):
    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    global deckImg
    deckImg = pygame.image.load('deck_image.png')
    uno_window.blit(deckImg, (width,height))


def add_screen():
    global uno_window
    uno_window = pygame.display.set_mode((x, y)) #creates a window with specified resolution (x,y)
    uno_window.fill(white)
    pygame.display.set_caption('Python UNO') #sets window title
    fps = pygame.time.Clock() #creates a clock that counts fps
    fps.tick(60)
    backgroundImg = pygame.image.load('background_image.png')
    displayimage(backgroundImg, x, y)
    #pygame.display.update()


def turnswitcher():
    pass

def createbutton(button_name,x1,y2,w1,h2,inactive_colour,active_colour,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x1+w1 > mouse[0] > x1 and y2+h2 > mouse[1] > y2:
        pygame.draw.rect(uno_window, active_colour,(x1,y2,w1,h2))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(uno_window, inactive_colour,(x1,y2,w1,h2))

    button_font_size = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(button_name, button_font_size)
    textRect.center = ( (x1+(w1/2)), (y2+(h2/2)) )
    uno_window.blit(textSurf, textRect)

def startup_menu():
    add_screen()
    startup = True
    while startup:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gametext_display('Welcome to UNO',2,2,50)
        singeplayer_button = createbutton('SINGLEPLAYER',150,450,100,50,green,orange,singleplayer)
        mutliplayer_button = createbutton('MULTILPLAYER',370,450,100,50,blue,orange,multiplayer)
        quit_button = createbutton('QUIT',550,450,100,50,red,orange,quitgame)
        pygame.display.update()

def quitgame():
    pygame.quit()
    quit()

def singleplayer():
    add_screen()
    play = True
    while play == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                deal_deck_selected()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                discard_card_selected()
        gametext_display('Player1', 12, 12, 15)
        gametext_display('Computer', 1.2, 12, 15)
        width = (x/2.3) #location on screen
        height = (y/3) #location on screen
        deck_image(width,height)
        pygame.display.update()

def empty_singleplayer_screen():
    add_screen()
    gametext_display('Player1', 12, 12, 15)
    gametext_display('Computer', 1.2, 12, 15)
    width = (x/2.3) #location on screen
    height = (y/3) #location on screen
    deck_image(width,height)

        


def multiplayer():
    add_screen()
    startup = True
    while startup:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        multiplayer_local_button = createbutton('Multiplayer Local',250,450,100,50,blue,orange,multiplayer_local)
        multiplayer_online_button = createbutton('Multiplayer Online',500,450,100,50,blue,orange,multiplayer_online)
        pygame.display.update()

def multiplayer_local():
    pass

def multiplayer_online():
    pass

def uno_gui():
    startup_menu()

uno_gui()
#cards = uno_card_images_dict()
#print(cards)
#uno_card_images_dict()
