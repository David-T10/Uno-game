import random
import pygame
import os
import time
import pickle
import socket
from tkinter import *
from tkinter import messagebox as ms
import sqlite3
from sys import exit
from networkclass import Network
from player import MOplayer
from _thread import *
#imported modules necessary for game's function

pygame.mixer.pre_init(44100,16,2,4096) #initialises pygame mixer for music
pygame.init() #initialises pygame


skipturn = False #variable used to check if a skip action card has been played
reverseturn = False #variable used to check if a skip reverse card has been played
p1reverseturn = False
p1skipturn = False 
p2reverseturn = False
p2skipturn = False
Playerwins = False  #variable used to check if Player has won
Computerwins = False   #variable used to check if Computer has won
Player1wins = False #variable used to check if Player1 in multiplayer has won
Player2wins = False #variable used to check if Player2 in multiplayer has won
Score = 0 #placeholder for score value for users (yet to be added t table)
x = 800 #screen resolution width
y = 600 #screen resolution height
div_iwidth = 750 #adjustment to width for dispalying images
div_iheight = 550 #adjustment to height for dispalying images
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
orange = (255,165,0)  #predefined colours
mouseposition = pygame.mouse.get_pos() #gets mouse position

class Card: 
    def __init__(self, suit, number): #Card given the attribute Suit and Number
        self.suit = suit
        vals = {10: "reverse", 11:"skip", 12:"+2"} #dictionary to store action card values paired with number keys
        if type(number) is int:
            if number < 10:
                self.number = str(number)
            else:
                self.number = vals[number] #used when building the deck of cards, to create action cards using above dictionary
        self.image = pygame.image.load(str(self) + ".png") #load each creating image into the program according to the card name

    def __eq__(self, other):
        if self.suit == other.suit and self.number == other.number: 
            return True
        return False

    def __repr__(self):
        return self.showcard()

    def getImage():
        return self.image

    def showcard(self):
        return "{} {}".format(self.suit, self.number) #returns value of a created Card in a printed format

class Deck:
    def __init__(self):    
        self.cards = [] #an array stored all the card values
        self.builddeck() 

    def builddeck(self):
        for s in ["yellow","red","blue","green"]:
            for n in range(0,13):
                self.cards.append(Card(s, n))   #builds a deck by pairing each colour with numbers from 0 to 12, then converting them into a Card object and adding them to an array of card

    def showdeck(self):
        for card in self.cards:
            print(card)  #when showdeck is called, it will display all cards in the self.cards array

    def shuffle(self):
        random.shuffle(self.cards) #uses random to shuffle order of cards array

    def drawcard(self):
        return self.cards.pop()  #removes last card in cards array and returns the value



class Player:
    def __init__(self, name):
        self.hand = [] #array for player's hand
        self.name = name  

    def draw(self, deck, x):
        for i in range(x):
            self.hand.append(deck.drawcard())
            #allows player draw multiple cards and appends them into hand array


    def showhand(self):
      print("{} Hand is: ".format(self.name))
      h=30
      for card in self.hand:
          print(card)
          maingame.displayimage(card.image,div_iwidth,div_iheight-h) #display's each card in a player's hand on to the game screen
          pygame.display.update()
          h=h+25 #moves each following card down by 25 to ensure the user can see all the cards
      #if len(self.hand) == 1:
      #   global UNO_called
      #   while UNO_called == False:
      #      gamtext_display("Press U to call UNO", 2,4,15)
       #     print("call uno thing")
       #     #pygame.display.update()
       #     if UNO_called == True:
       #         gametext_display("UNO CALLED", 2,5, 15)
       #         break
       #  pygame.display.update()   UNO CALLED FUNCTION NOT WORKING, WILL FIX
        
      if len(self.hand) == 0:
        Playerwins = True
        add_screen()
        maingame.gametext_display("Player1 won. Game Over", 2, 2, 40)
        maingame.gametext_display("Score: +100 ", 2,4,40)
        pygame.mixer.music.load("winnermusic.mp3")
        pygame.mixer.music.play(-1)
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        os._exit(1)
        #once a player has no cards in their hand, Player has won, displays win screen and plays winner music


    def discard(self):
      global skipturn
      global reverseturn
      if len(self.hand) != 0:
        discard_card = self.hand[maingame.down]
        self.throwAway(discard_card) #if the player has cards left in their hand, it will discard the card based on their keyboard input using throwAway
        
       
    def throwAway(self, discard):
       global maingamepile
       if len(maingamepile) > 1: #checks if there is a card or cards in play already
        lastcardplaced = maingamepile[-1] #if there is then the last card on the pile = the last card placed
        for card in self.hand:
            if card == discard: 
                if card.number == lastcardplaced.number or card.suit == lastcardplaced.suit: #checks if card selected to be discarded has the same suit or number as the last card in play on the pile
                    if card.number == "+2":
                        maingame.gametext_display("Computer Draws 2 more cards", 2, 4,15)
                        pygame.display.update()
                        Computer.draw(deck, 2) #if card is a +2, computer gets 2 more cards
                    elif card.number == "skip":
                        skipturn = True
                        maingame.gametext_display("Computer's Turn Will Be Skipped Next Round", 2, 4,15)
                        pygame.display.update() #if card is a skip, computer's turn will be skipped next in the main game loop
                    elif card.number == "reverse":
                        reverseturn = True
                        maingame.gametext_display("Computer's Turn Will Be Reversed Next Round", 2,4,15)
                        pygame.display.update() #if card is a reverse, computer's turn will be reversed next in the main game loop (effectively player gets another free turn)
                    self.hand.remove(card) #card is removed from player's hand
                    maingamepile.append(card) #card is added on to main game pile
                    break
                else:
                    invalidturn = True  
                    maingame.gametext_display("Invalid move. 1 card added to hand.",2,5,15)
                    pygame.display.update()
                    Player1.draw(deck, 1)
                    break  #if the user selects a card that isn't the same suit or number the card is invalidly played and they will face a draw card penalty
       else:
        for card in self.hand:
           if card == discard:
            self.hand.remove(card)
            maingamepile.append(card) #if there are no cards in play on the main game pile then the card the user selects will be discarded as normal (as this means the user is starting the game first)
            
class Playerone(Player):
    def throwAway(self, discard):
       global maingamepile
       if len(maingamepile) > 1: #checks if there is a card or cards in play already
        lastcardplaced = maingamepile[-1] #if there is then the last card on the pile = the last card placed
        for card in self.hand:
            if card == discard: 
                if card.number == lastcardplaced.number or card.suit == lastcardplaced.suit: #checks if card selected to be discarded has the same suit or number as the last card in play on the pile
                    if card.number == "+2":
                        maingame.gametext_display("Player2 Draws 2 more cards", 2, 4,15)
                        pygame.display.update()
                        mPlayer2.draw(deck, 2) #if card is a +2, computer gets 2 more cards
                    elif card.number == "skip":
                        p1skipturn = True
                        maingame.gametext_display("Player2's Turn Will Be Skipped Next Round", 2, 4,15)
                        pygame.display.update() #if card is a skip, computer's turn will be skipped next in the main game loop
                    elif card.number == "reverse":
                        p1reverseturn = True
                        maingame.gametext_display("Player2's Turn Will Be Reversed Next Round", 2,4,15)
                        pygame.display.update() #if card is a reverse, computer's turn will be reversed next in the main game loop (effectively player gets another free turn)
                    self.hand.remove(card) #card is removed from player's hand
                    maingamepile.append(card) #card is added on to main game pile
                    break
                else:
                    p1invalidturn = True  
                    maingame.gametext_display("Invalid move. 1 card added to hand.",2,5,15)
                    pygame.display.update()
                    mPlayer1.draw(deck, 1)
                    break  #if the user selects a card that isn't the same suit or number the card is invalidly played and they will face a draw card penalty
       else:
        for card in self.hand:
           if card == discard:
            self.hand.remove(card)
            maingamepile.append(card) #if there are no cards in play on the main game pile then the card the user selects will be discarded as normal (as this means the user is starting the game first)
    
    def showhand(self):
      print("{} Hand is: ".format(self.name))
      h=30
      for card in self.hand:
          print(card)
          maingame.displayimage(card.image,div_iwidth,div_iheight-h) #display's each card in a player's hand on to the game screen
          pygame.display.update()
          h=h+25 #moves each following card down by 25 to ensure the user can see all the cards
        
      if len(self.hand) == 0:
        Player1wins = True
        add_screen()
        maingame.gametext_display("Player1 won. Game Over", 2, 2, 40)
        maingame.gametext_display("Score: +100 ", 2,4,40)
        pygame.mixer.music.load("winnermusic.mp3")
        pygame.mixer.music.play(-1)
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        os._exit(1)
        #once a player has no cards in their hand, Player has won, displays win screen and plays winner music

class Player2(Player):
    def discard(self):
        if len(self.hand) != 0:
            discard_card = self.hand[maingame.down]
            self.throwAway(discard_card) #if the player has cards left in their hand, it will discard the card based on their keyboard input using throwAway
            multiplayergame.p2turn = False
        return multiplayergame.p2turn

    def throwAway(self, discard):
       global maingamepile
       if len(maingamepile) > 1: #checks if there is a card or cards in play already
        lastcardplaced = maingamepile[-1] #if there is then the last card on the pile = the last card placed
        for card in self.hand:
            if card == discard: 
                if card.number == lastcardplaced.number or card.suit == lastcardplaced.suit: #checks if card selected to be discarded has the same suit or number as the last card in play on the pile
                    if card.number == "+2":
                        maingame.gametext_display("Player1 Draws 2 more cards", 2, 4,15)
                        pygame.display.update()
                        mPlayer2.draw(deck, 2) #if card is a +2, computer gets 2 more cards
                    elif card.number == "skip":
                        p2skipturn = True
                        maingame.gametext_display("Player1's Turn Will Be Skipped Next Round", 2, 4,15)
                        pygame.display.update() #if card is a skip, computer's turn will be skipped next in the main game loop
                    elif card.number == "reverse":
                        p2reverseturn = True
                        maingame.gametext_display("Player1's Turn Will Be Reversed Next Round", 2,4,15)
                        pygame.display.update() #if card is a reverse, computer's turn will be reversed next in the main game loop (effectively player gets another free turn)
                    self.hand.remove(card) #card is removed from player's hand
                    maingamepile.append(card) #card is added on to main game pile
                    break
                else:
                    invalidturn = True  
                    maingame.gametext_display("Invalid move. 1 card added to hand.",2,5,15)
                    pygame.display.update()
                    mPlayer2.draw(deck, 1)
                    break  #if the user selects a card that isn't the same suit or number the card is invalidly played and they will face a draw card penalty
       else:
        for card in self.hand:
           if card == discard:
            self.hand.remove(card)
            maingamepile.append(card) #if there are no cards in play on the main game pile then the card the user selects will be discarded as normal (as this means the user is starting the game first)
         
        
    def showhand(self):
        #deckImg = pygame.image.load('deck_image.png')
        print("{}'s Hand is: ".format(self.name))
        h=30
        for card in self.hand:
            print(card)
            maingame.displayimage(card.image,div_iwidth-600,div_iheight-h) #parameters altered slightly to images displayed on the right hand side of the screen
            pygame.display.update()
            h=h+25
        if len(self.hand) == 0:
            Player2wins = True
            add_screen()
            maingame.gametext_display("Player2 won. Game Over", 2, 2, 40)
            maingame.gametext_display("Score: +100 ", 2,4,40)
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
            os._exit(1) 
            #similar to Player showhand
        

    
class AI(Player):
    def discard(self):
        global maingamepile
        lastcardplaced = maingamepile[-1]
        print("lastplayed card is", lastcardplaced)
        for i in range (len(self.hand)):
            ai_card = self.hand[i]
            if ai_card.suit == lastcardplaced.suit or ai_card.number == lastcardplaced.number: #checks if card the computer wants to discard is the same suit or number as the card the player first discarded
                print("computer discarded", ai_card)
                self.aithrowAway(ai_card)
                if ai_card.number == "+2":
                    maingame.gametext_display("Player1 Draws 2 more cards", 2, 5,15)
                    pygame.display.update()
                    Player1.draw(deck, 2)
                elif ai_card.number == "skip":
                    maingame.gametext_display("Player1's Turn Skipped", 2, 5,15)
                    Computerskip = True
                    pygame.display.update()
                    Computer.discard()
                elif ai_card.number == "reverse":
                    maingame.gametext_display("Player1's Turn Reversed", 2,5,15)
                    Computerreverse = True
                    pygame.display.update()
                    Computer.discard() 
            else:
                maingame.gametext_display("Computer draws a card", 2, 7, 15)
                Computer.draw(deck, 1)
                Computer.showhand()
                break
            break 
            #works similarly to the Player discard function. Check card suit, number and follows UNO rules accordingly 
        
    def aithrowAway(self, discard):
        for card in self.hand:
            if card == discard:
              self.hand.remove(card)
              maingamepile.append(card) #removes card from hand and places in main game pile


    def showhand(self):
        print("{}'s Hand is: ".format(self.name))
        h=30
        for card in self.hand:
            print(card)
            maingame.displayimage(deckImg,div_iwidth-600,div_iheight-h) #parameters altered slightly to images displayed on the right hand side of the screen
            pygame.display.update()
            h=h+25
        if len(self.hand) == 0:
            Computerwins = True
            add_screen()
            maingame.gametext_display("Computer won. Game Over", 2, 2, 40)
            maingame.gametext_display("Score: +100 ", 2,4,40)
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
            os._exit(1) 
            #similar to Player showhand 
    
deck = Deck() #initialises deck
maingamepile = [] #initialises maingamepile
Player1 = Player('Player1')
Computer = AI('Computer')
#singleplayer stuff

mdeck = Deck()
mdeck.shuffle()
mPlayer1 = Playerone("Player1")
mPlayer2 = Player2("Player2")
mPlayer1.draw(mdeck , 7)
mPlayer2.draw(mdeck , 7)
#initialises players for multiplayer game

#GUI + EXTRA FUNCTION STUFF
    

class maingame: #class for main game functionality, OOP required for multiplayer purposes
    def __init__(self):
        self.iwidth = iwidth
        self.iheight = iheight
        self.width = width
        self.height = height
        self.gametext = gametext
        self.textSurface = textSurface
        self.lastcardplaced = lastcardplaced
        self.fps = fps
        self.backgroundImg = backgroundImg
        self.mouse = mouse
        self.click = click
        self.button_font_size = button_font_size
        self.down = down
        #all variables defined in my main game that aren't already globalised
        #below are the methods used in my game
        
    def displayimage(image_name,div_iwidth, div_iheight): #displaying imaages (UNO cards) on the screen
        maingame.iwidth = x-div_iwidth
        maingame.iheight = y-div_iheight
        uno_window.blit(image_name, (maingame.iwidth,maingame.iheight))
        time.sleep(0.3)

    def text_objects(text, font): #this function takes the rectangle and puts it over the whole of the text so it can be moved as one
        maingame.textSurface = font.render(text, True, black)
        return maingame.textSurface, maingame.textSurface.get_rect()

    def gametext_display(text,divby_x,divby_y,fontsize): #displaying text on the screen
        maingame.gametext = pygame.font.Font('freesansbold.ttf', fontsize)
        TextSurf,TextRect = maingame.text_objects(text, maingame.gametext)
        TextRect.center = ((x/divby_x) ,(y/divby_y))
        uno_window.blit(TextSurf, TextRect)

    def deal_deck_selected():
            numofcards = int(input("How many cards to you want dealt to each player? (max 9): "))
            deck.shuffle()
            Player1.draw(deck, numofcards)
            Player1.showhand()
            Computer.draw(deck, numofcards)
            Computer.showhand()
            maingame.gametext_display('Player1 starts first, use the number keys to select a card',2,12,15)
            #when the TAB key is pressed my program jumps to this function which deals cards to each Player and displays their hand to the screen
            
                                   
    def display_last_discarded():
        global maingamepile
        maingame.lastcardplaced = maingamepile[-1]
        maingame.displayimage(maingame.lastcardplaced.image, div_iwidth-300, div_iheight-150)
        maingame.gametext_display("Last placed card is:", 2, 3.5, 15)
        pygame.display.update()
        #an image of the last card in play will be displayed to the screen

    def discard_card_selected(): #singleplayer turn controller
        global skipturn
        global reverseturn
        global computerreverse
        global computerskip
        global invalidturn
        if Player1wins == False and Computerwins == False and skipturn == False and reverseturn == False:
            Player1.discard()
            Computer.discard()
            maingame.empty_singleplayer_screen()
            Player1.showhand()
            Computer.showhand()
            maingame.display_last_discarded()
            time.sleep(2.5)
            #If no one has won and no action cards have been played (excluded +2), gameplay will run as normal.
        elif skipturn == True:
            Player1.discard()
            skipturn = False
            #if a player plays a skip card then skipturn will become True, when the user selects a card to play, they will be able to discard another one and the computer won't
        elif reverseturn == True:
            Player1.discard()
            reverseturn = False #works the same as the skip section above
        elif computerskip == True:
            Computer.discard()
            computerskip = False
        elif computerreverse == True:
            Computer.discard()
            computerreverse = False
        elif invalidturn == True:
            Player1.discard()
            Computer.discard()
            #once the user is punished for making an invalid move, both will be able to play cards as normal
    

    def deck_image(width,height):
        global deckImg
        deckImg = pygame.image.load('deck_image.png')
        uno_window.blit(deckImg, (width,height))
        #blank uno card image to visually represent the 'pile'


    def add_screen():
        global uno_window
        uno_window = pygame.display.set_mode((x, y)) #creates a window with specified resolution (x,y)
        uno_window.fill(white)
        pygame.display.set_caption('Python UNO') #sets window title
        maingame.fps = pygame.time.Clock() #creates a clock that counts fps
        maingame.fps.tick(20)
        maingame.backgroundImg = pygame.image.load('background_image.png')
        maingame.displayimage(maingame.backgroundImg, x, y)
        pygame.display.update()
        #used to completely update a screen (as images can't be removed from a screen in pygame)
        #acts as a blank template


    def createbutton(button_name,x1,y2,w1,h2,inactive_colour,active_colour,action=None):
        maingame.mouse = pygame.mouse.get_pos()
        maingame.click = pygame.mouse.get_pressed()
        if x1+w1 > maingame.mouse[0] > x1 and y2+h2 > maingame.mouse[1] > y2:
            pygame.draw.rect(uno_window, active_colour,(x1,y2,w1,h2))
            if maingame.click[0] == 1 and action != None:
                action()
        else:
            pygame.draw.rect(uno_window, inactive_colour,(x1,y2,w1,h2))
        #checks if mouse position is within button's defined region and if so, colour will change, if the button is clicked then the defined action will be performed

        maingame.button_font_size = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = maingame.text_objects(button_name, maingame.button_font_size)
        textRect.center = ( (x1+(w1/2)), (y2+(h2/2)) )
        uno_window.blit(textSurf, textRect)
        #defines button text font and size and adds it the surface of the screen

    def startup_menu():
        maingame.add_screen()
        pygame.mixer.music.load("Menumusic.mp3")
        pygame.mixer.music.play(-1)
        startup = True
        while startup:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    #if the user clicks the x on the window the window will close and the game will quit
            maingame.gametext_display('Welcome to UNO',2,2,50)
            singeplayer_button = maingame.createbutton('SINGLEPLAYER',50,450,160,50,green,orange,maingame.singleplayer)
            mutliplayer_button = maingame.createbutton('MULTILPLAYER',250,450,160,50,blue,orange,multiplayergame.multiplayer_startup_screen)
            quit_button = maingame.createbutton('QUIT',450,450,100,50,red,orange,maingame.quitgame)
            help_button = maingame.createbutton('HELP', 600,450,100, 50, white, orange,maingame.help_screen)
            pygame.display.update()

        #main menu - plays main menu music and displays singleplayer,multiplaer,quit and help button

    def quitgame():
        pygame.quit()
        quit()
        #action for quit button to exit game

    def help_screen():
        maingame.add_screen()
        startup = True
        while startup:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            back_button = maingame.createbutton('BACK',50,450,100,40,white, orange,maingame.startup_menu)
            rulescreen_button = maingame.createbutton('RULES',500,450,100,40,white,orange,maingame.rulescreen)
            maingame.gametext_display('KEYBINDS                             ACTIONS',2,12,25)
            maingame.gametext_display('Tab                                       Deal Cards', 2,6,18)
            maingame.gametext_display('x                     Discard Card x in Hand', 2,4,18)
            maingame.gametext_display('Space                                    Draw a card',2,3,18)
            maingame.gametext_display('s                           Show last played card',2,2.3,18)
            pygame.display.update()
            #action for help button, displays back button to main menu and rule button to rule screen and keybinds

    def rulescreen():
        maingame.add_screen()
        startup = True
        while startup:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            back_button = maingame.createbutton('BACK',50,450,100,40,white, orange,maingame.help_screen)
            maingame.gametext_display("Rules: The rules of uno are simple.", 3.5,12,20)
            maingame.gametext_display("Your aim is to get rid of your cards before your opponent.", 2.3,9,20)
            maingame.gametext_display("Start the game by pressing the TAB button",3.3,7,20)
            maingame.gametext_display("Press the numbers keys to discard a card, e.g. 3 will discard your third card", 2,6,20)
            maingame.gametext_display("If you can't match the colour or number of the card on the pile, press SPACE",2,5,20)
            maingame.gametext_display("to draw another card",4.5,4.5,20)
            maingame.gametext_display("if you play a wrong card, a draw will be drawn for you", 3,4,20)
            maingame.gametext_display("Action Cards: Reverse- Reverses the turn order",2.5,3.5,20)
            maingame.gametext_display("Skip - skips the opponents turn", 3.5,3,20)
            maingame.gametext_display("+2- your opponent gets two extra cards", 2.5,2.5,20)
            pygame.display.update()
            #action for rule button, explains the rules of UNO

    def singleplayer():
        pygame.mixer.music.load("Menumusic_2.mp3")
        pygame.mixer.music.play(-1)
        maingame.add_screen()
        play = True
        while play == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    maingame.deal_deck_selected()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    maingame.down = 0
                    maingame.discard_card_selected()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    maingame.down = 1
                    maingame.discard_card_selected()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    maingame.down = 2
                    maingame.discard_card_selected()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    maingame.down = 3
                    maingame.discard_card_selected()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                    maingame.down = 4
                    maingame.discard_card_selected()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                    maingame.down = 5
                    maingame.discard_card_selected()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                    maingame.down = 6
                    maingame.discard_card_selected()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_8:
                    maingame.down = 7
                    maingame.discard_card_selected()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_9:
                    maingame.down = 8
                    maingame.discard_card_selected()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                    maingame.down = 9
                    maingame.discard_card_selected()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    maingame.display_last_discarded()
                    time.sleep(4)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    Player1.draw(deck, 1)
                    Player1.showhand()
                    maingame.gametext_display("You've drawn a card from the pile",2,5,15)
                    Computer.discard()
                    Computer.showhand()
                #checks what number in the list of cards the user has selected to remove, and removes that card from their hand
                #pressing space draws a card for the user at any point in the game
                #pressing s displays the last card in play for 4 seconds as a reminder
                    
                '''elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                    global Uno_called
                    UNO_called = True'''
            maingame.gametext_display('Player1', 12, 12, 15)
            maingame.gametext_display('Computer', 1.2, 12, 15)
            back_button = maingame.createbutton('BACK',300,500,200,40,white, orange,maingame.startup_menu) #back button to main menu
            maingame.width = (x/2.3) #location on screen
            maingame.height = (y/3) #location on screen
            maingame.deck_image(maingame.width,maingame.height) #blank UNO CARD image to represent pile
            pygame.display.update()
                


    def empty_singleplayer_screen():
        maingame.add_screen()
        maingame.gametext_display('Player1', 12, 12, 15)
        maingame.gametext_display('Computer', 1.2, 12, 15)
        maingame.width = (x/2.3) #location on screen
        maingame.height = (y/3) #location on screen
        maingame.deck_image(maingame.width,maingame.height)
        #blank template for singleplayer screen, used after cards have been discarded to refresh view

    def uno_gui():
        maingame.startup_menu()

class Multiplayeronline(maingame):
    def __init__(self):
        pass

    def empty_multiplayer_online_screen():
        maingame.add_screen()
        maingame.gametext_display('Player1', 12, 12, 15)
        maingame.gametext_display('Player2', 1.2, 12, 15)
        maingame.width = (x/2.3)
        maingame.height = (y/3)
        maingame.deck_image(maingame.width,maingame.height)

    def MOgameplay():
        Multiplayeronline.main()
        maingame.add_screen()
        global multiplayeronline
        global firstplayerobject
        global secondplayerobject
        multiplayeronline = True
        firstplayerobject.draw(deck, 5)
        secondplayerobject.draw(deck, 5)
        firstplayerobject.showhand()
        while multiplayeronline ==  True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    Multiplayeronline.down = 0
                    Multiplayeronline.gamemanager()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    Multiplayeronline.down = 1
                    multiplayergame.gamemanager()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    Multiplayeronline.down = 2
                    Multiplayeronline.main()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    Multiplayeronline.down = 3
                    Multiplayeronline.main()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                    Multiplayeronline.down = 4
                    Multiplayeronline.main()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                    Multiplayeronline.down = 5
                    Multiplayeronline.main()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                    Multiplayeronline.down = 6
                    Multiplayeronline.main()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_8:
                    Multiplayeronline.down = 7
                    Multiplayeronline.main()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_9:
                    Multiplayeronline.down = 8
                    Multiplayeronline.main()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                    Multiplayeronline.down = 9
                    Multiplayeronline.main()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    Multiplayeronline.display_last_discarded()
                    time.sleep(4)

            maingame.gametext_display('Player1', 12, 12, 15)
            maingame.gametext_display('Player2', 1.2, 12, 15)
            maingame.width = (x/2.3)
            maingame.height = (y/3)
            maingame.deck_image(maingame.width,maingame.height)
            pygame.display.update()

    def gamemanager(self):
        global firstplayerobject
        global secondplayerobject
        firstplayerobject.showhand()
        secondplayerobject.showhand()

    def MOwinnerscreen(playerthatwon):
        maingame.add_screen()
        maingame.gametext_display(playerthatwon," won. Game Over", 2, 2, 40)
        gametext_display("Score: +100 ", 2,4,40)
        pygame.mixer.music.load("winnermusic.mp3")
        pygame.mixer.music.play(-1)
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        os._exit(1)
        #once player has no cards in their hand, Player has won, displays win screen and plays winner music

    def main(): #ADD USER GAMEPLAY BETWEEN SERVERS AND THEN TEST EVERYTHING
        pygame.mixer.music.load("Menumusic_2.mp3")
        pygame.mixer.music.play(-1)
        host = socket.gethostname()
        ip = socket.gethostbyname(host)
        run = True
        try:
            n = Network(ip)
            p = get.pnumber()
            print(p)
            print(p['Player'])
            firstplayerobject = p['Player']
        except:
            print("Can't connect to server")
        while run:
            player2 = n.send(p)
            secondplayerobject = p2['Player']
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
            if firstplayerobject.won == True: 
                run = False
                Multiplayeronline.MOwinnerscreen(firstplayerobject)
            elif secondplayerobject.won == True:
                run = False
                Multiplayeronline.MOwinnerscreen(secondplayerobject)
            else:
                Multiplayeronline.MOgameplay()
            pygame.display.update()


class multiplayergame(maingame): #class for multiplayer including main game functionality
    def __init__(self):
        self.deck = Deck()
        self.maingamepile = []
        self.p1turn = False
        self.p2turn = False

    def multiplayer_startup_screen():
        maingame.add_screen()
        multiplayer_selected = True
        while multiplayer_selected == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            multiplayer_local_button = maingame.createbutton('Multiplayer Local', 150,450,160,50,blue,orange,multiplayergame.multiplayer_gui)
            multiplayer_online_button = maingame.createbutton('Multiplayer Online', 450,450,160,50,red,orange,Multiplayeronline.MOgameplay)
            pygame.display.update()

    def empty_multiplayer_screen():
        maingame.add_screen()
        maingame.gametext_display('Player1', 12, 12, 15)
        maingame.gametext_display('Player2', 1.2, 12, 15)
        maingame.width = (x/2.3)
        maingame.height = (y/3)
        maingame.deck_image(maingame.width,maingame.height)
        mPlayer1.showhand()
        mPlayer2.showhand()
            
    def multiplayer_gui():
        print("connecting..")
        time.sleep(3)
        print("connected")
        global mdeck
        global mPlayer1
        global mPlayer2
        pygame.mixer.music.load("Menumusic_2.mp3")
        pygame.mixer.music.play(-1)
        multiplayergame.empty_multiplayer_screen()
        maingame.gametext_display('Player1 starts first', 2, 12,15)
        multiplayergame.p1turn = True
        multiplayergame.p2turn = False
        global start
        start = True
        while start == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                    maingame.down = 0
                    multiplayergame.gamemanager()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                    maingame.down = 1
                    multiplayergame.gamemanager()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                    maingame.down = 2
                    multiplayergame.gamemanager()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                    maingame.down = 3
                    multiplayergame.gamemanager()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                    maingame.down = 4
                    multiplayergame.gamemanager()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                    maingame.down = 5
                    multiplayergame.gamemanager()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                    maingame.down = 6
                    multiplayergame.gamemanager()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_8:
                    maingame.down = 7
                    multiplayergame.gamemanager()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_9:
                    maingame.down = 8
                    multiplayergame.gamemanager()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                    maingame.down = 9
                    multiplayergame.gamemanager()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    multiplayergame.display_last_discarded()
                    time.sleep(4)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if multiplayergame.p1turn == True:
                        mPlayer1.draw(deck, 1)
                        multiplayergame.gametext_display("Player1 draw's a card", 2, 5, 15)
                        multiplayergame.empty_multiplayer_screen()
                    elif multiplayergame.p2turn == True:
                        mPlayer2.draw(deck, 1)
                        multiplayergame.gametext_display("Player2 draw's a card",2,5,15)
                        multiplayergame.empty_multiplayer_screen()
                #checks what number in the list of cards the user has selected to remove, and removes that card from their hand
                #pressing space draws a card for the user at any point in the game
                #pressing s displays the last card in play for 4 seconds as a reminder
            maingame.gametext_display('Player1', 12, 12, 15)
            maingame.gametext_display('Player2', 1.2, 12, 15)
            maingame.width = (x/2.3) #location on screen
            maingame.height = (y/3) #location on screen
            maingame.deck_image(maingame.width,maingame.height) #blank UNO CARD image to represent pile
            back_button = maingame.createbutton('BACK',300,500,200,40,white, orange,maingame.startup_menu) #back button to main menu
            pygame.display.update()
        #multiplayer local main screen and functionality
        
    def gamemanager():
        global p1reverseturn
        global p1skipturn
        global p2reverseturn
        global p2skipturn
        #global netconnection
        if start == True:
            if multiplayergame.p1turn == True and multiplayergame.p2turn == False and p1reverseturn == False and p1skipturn == False and p2reverseturn == False and p2skipturn == False:
                maingame.gametext_display("Player1's turn", 2,5,15)
                mPlayer1.discard()
                multiplayergame.p1turn = False
                multiplayergame.p2turn = True
                maingame.gametext_display("End of Player1's Turn", 2,3,15)
                multiplayergame.empty_multiplayer_screen()
            elif multiplayergame.p2turn == True and multiplayergame.p1turn == False and p1reverseturn == False and p1skipturn == False and p2reverseturn == False and p2skipturn == False:
                maingame.gametext_display("Player2's turn", 2,5,15)
                mPlayer2.discard()
                multiplayergame.p1turn = True
                maingame.gametext_display("End of Player2's Turn", 2,3,15)
                multiplayergame.empty_multiplayer_screen()
            elif multiplayergame.p1turn == True and multiplayergame.p2turn == False and (p1reverseturn == True or p1skipturn == True):
                mPlayer1.discard()
            elif multiplayergame.p2turn == True and multiplayergame.p1turn == False and (p2reverseturn == True or p2skipturn == True):
                mPlayer2.discard()
        #manages who''s turn it is between each player and what certain playing cards result in


maingame.uno_gui()



# make database and users (if not exists already) table at programme start up
with sqlite3.connect('uno_user_database.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT NOT NULL ,password TEXT NOT NULL, userscore INTEGER);')
db.commit()
db.close()
#creates a table with 4 columns, userid, username, password and score

#login class for uno
class Unologin:
    def __init__(self,master):
    	# Window 
        self.master = master
        # Some Usefull variables
        self.username = StringVar()
        self.password = StringVar()
        self.userscore = IntVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        #Create Widgets
        self.widgets()

    #Login Function
    def login(self):
    	#Establish Connection
        with sqlite3.connect('uno_user_database.db') as db:
            c = db.cursor()

        #Find user if there is any, if username and password exist, log in else username not found
        find_user = ('SELECT * FROM users WHERE username = ? and password = ?')
        c.execute(find_user,[(self.username.get()),(self.password.get())])
        result = c.fetchall()
        if result:
            self.logf.pack_forget()
            self.head['text'] = self.username.get() + '\n Logged In'
            self.head['pady'] = 100
            self.head['padx'] = 100
            global login
            login = True
            maingame.uno_gui()
        else:
            ms.showerror('Username Not Found.')
            
    def new_user(self):
    	#Establish Connection
        with sqlite3.connect('uno_user_database.db') as db:
            c = db.cursor()

        #Find Existing username if user enters name that already exists, they must try another one else success
        find_user = ('SELECT * FROM users WHERE username = ?')
        c.execute(find_user,[(self.username.get())])        
        if c.fetchall():
            ms.showerror('Error!','Username Taken Try a Diffrent One.')
        else:
            ms.showinfo('Success!')
            self.log()
        #Create New Account 
        insert = 'INSERT INTO users(username,password) VALUES(?,?)'
        c.execute(insert,[(self.n_username.get()),(self.n_password.get())])
        db.commit()

        #Frame Packing Methords
    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'LOGIN'
        self.logf.pack()
    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Create Account'
        self.crf.pack()
        
    #Draw Widgets
    def widgets(self):
        self.head = Label(self.master,text = 'LOGIN',font = ('',35),pady = 10)
        self.head.pack()
        self.logf = Frame(self.master,padx =10,pady = 10)
        Label(self.logf,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.username,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.logf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.logf,textvariable = self.password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
        Button(self.logf,text = ' Login ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.login).grid()
        Button(self.logf,text = ' Create Account ',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.cr).grid(row=2,column=1)
        self.logf.pack()
        
        self.crf = Frame(self.master,padx =10,pady = 10)
        Label(self.crf,text = 'Username: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_username,bd = 5,font = ('',15)).grid(row=0,column=1)
        Label(self.crf,text = 'Password: ',font = ('',20),pady=5,padx=5).grid(sticky = W)
        Entry(self.crf,textvariable = self.n_password,bd = 5,font = ('',15),show = '*').grid(row=1,column=1)
        Button(self.crf,text = 'Create Account',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.new_user).grid()
        Button(self.crf,text = 'Go to Login',bd = 3 ,font = ('',15),padx=5,pady=5,command=self.log).grid(row=2,column=1)


    

#create log in window and application object
'''root = Tk()
root.title("Login Form")
Unologin(root)
root.mainloop()'''





