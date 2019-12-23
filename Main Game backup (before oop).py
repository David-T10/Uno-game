import random
import pygame
import os
import time  
from tkinter import *
from tkinter import messagebox as ms
import sqlite3
from sys import exit
#from network_file import Network
#imported modules necessary for game's function

pygame.mixer.pre_init(44100,16,2,4096) #initialises pygame mixer for music
pygame.init() #initialises pygame

#ClientNumber = 0 #multiplayer client test
skipturn = False #variable used to check if a skip action card has been played
reverseturn = False #variable used to check if a skip reverse card has been played
Player1wins = False  #variable used to check if Player has won
Computerwins = False   #variable used to check if Computer has won
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
          displayimage(card.image,div_iwidth,div_iheight-h) #display's each card in a player's hand on to the game screen
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
        Player1wins = True
        add_screen()
        gametext_display("Player1 won. Game Over", 2, 2, 40)
        gametext_display("Score: +100 ", 2,4,40)
        pygame.mixer.music.load("winnermusic.mp3")
        pygame.mixer.music.play(-1)
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        os._exit(1)
        #once a player has no cards in their hand, Player has won, displays win screen and plays winner music


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
                    gametext_display("Player1 Draws 2 more cards", 2, 5,15)
                    pygame.display.update()
                    Player1.draw(deck, 2)
                elif ai_card.number == "skip":
                    gametext_display("Player1's Turn Skipped", 2, 5,15)
                    Computerskip = True
                    pygame.display.update()
                    Computer.discard()
                elif ai_card.number == "reverse":
                    gametext_display("Player1's Turn Reversed", 2,5,15)
                    Computerreverse = True
                    pygame.display.update()
                    Computer.discard() 
            else:
                gametext_display("Computer draws a card", 2, 5, 15)
                Computer.draw(deck, 1)
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
            displayimage(deckImg,div_iwidth-600,div_iheight-h) #parameters altered slightly to images displayed on the right hand side of the screen
            pygame.display.update()
            h=h+25
        if len(self.hand) == 0:
            Computerwins = True
            add_screen()
            gametext_display("Computer won. Game Over", 2, 2, 40)
            gametext_display("Score: +100 ", 2,4,40)
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
            os._exit(1) 
            #similar to Player showhand 
        
deck = Deck() #initialises deck
maingamepile = [] #initialises maingamepile
Player1 = Player('Player1') 
Computer = AI('Computer')

#GUI + EXTRA FUNCTION STUFF

def displayimage(image_name,div_iwidth, div_iheight): #displaying imaages (UNO cards) on the screen
    iwidth = x-div_iwidth
    iheight = y-div_iheight
    uno_window.blit(image_name, (iwidth,iheight))
    time.sleep(0.3)

def text_objects(text, font): #this function takes the rectangle and puts it over the whole of the text so it can be moved as one
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def gametext_display(text,divby_x,divby_y,fontsize): #displaying text on the screen
    gametext = pygame.font.Font('freesansbold.ttf', fontsize)
    TextSurf,TextRect = text_objects(text, gametext)
    TextRect.center = ((x/divby_x) ,(y/divby_y))
    uno_window.blit(TextSurf, TextRect)

def deal_deck_selected():
        numofcards = int(input("How many cards to you want dealt to each player? (max 9): "))
        deck.shuffle()
        Player1.draw(deck, numofcards)
        Player1.showhand()
        Computer.draw(deck, numofcards)
        Computer.showhand()
        gametext_display('Player1 starts first, use the number keys to select a card',2,12,15)
        #when the TAB key is pressed my program jumps to this function which deals cards to each Player and displays their hand to the screen
        
                               
def display_last_discarded():
    global maingamepile
    lastcardplaced = maingamepile[-1]
    displayimage(lastcardplaced.image, div_iwidth-300, div_iheight-150)
    gametext_display("Last placed card is:", 2, 3.5, 15)
    pygame.display.update()
    #an image of the last card in play will be displayed to the screen

def discard_card_selected(): #turn controller
    global skipturn
    global reverseturn
    global computerreverse
    global computerskip
    global invalidturn
    if Player1wins == False and Computerwins == False and skipturn == False and reverseturn == False:
        Player1.discard()
        Computer.discard()
        empty_singleplayer_screen()
        Player1.showhand()
        Computer.showhand()
        display_last_discarded()
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
        computer.discard()
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
    fps = pygame.time.Clock() #creates a clock that counts fps
    fps.tick(20)
    backgroundImg = pygame.image.load('background_image.png')
    displayimage(backgroundImg, x, y)
    pygame.display.update()
    #used to completely update a screen (as images can't be removed from a screen in pygame)
    #acts as a blank template


def createbutton(button_name,x1,y2,w1,h2,inactive_colour,active_colour,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x1+w1 > mouse[0] > x1 and y2+h2 > mouse[1] > y2:
        pygame.draw.rect(uno_window, active_colour,(x1,y2,w1,h2))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(uno_window, inactive_colour,(x1,y2,w1,h2))
    #checks if mouse position is within button's defined region and if so, colour will change, if the button is clicked then the defined action will be performed

    button_font_size = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(button_name, button_font_size)
    textRect.center = ( (x1+(w1/2)), (y2+(h2/2)) )
    uno_window.blit(textSurf, textRect)
    #defines button text font and size and adds it the surface of the screen

def startup_menu():
    add_screen()
    pygame.mixer.music.load("Menumusic.mp3")
    pygame.mixer.music.play(-1)
    startup = True
    while startup:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                #if the user clicks the x on the window the window will close and the game will quit
        gametext_display('Welcome to UNO',2,2,50)
        singeplayer_button = createbutton('SINGLEPLAYER',50,450,160,50,green,orange,singleplayer)
        mutliplayer_button = createbutton('MULTILPLAYER',250,450,160,50,blue,orange,multiplayer)
        quit_button = createbutton('QUIT',450,450,100,50,red,orange,quitgame)
        help_button = createbutton('HELP', 600,450,100, 50, white, orange,help_screen)
        pygame.display.update()

    #main menu - plays main menu music and displays singleplayer,multiplaer,quit and help button

def quitgame():
    pygame.quit()
    quit()
    #action for quit button to exit game

def help_screen():
    add_screen()
    startup = True
    while startup:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        back_button = createbutton('BACK',50,450,100,40,white, orange,startup_menu)
        rulescreen_button = createbutton('RULES',500,450,100,40,white,orange,rulescreen)
        gametext_display('KEYBINDS                             ACTIONS',2,12,25)
        gametext_display('Tab                                       Deal Cards', 2,6,18)
        gametext_display('x                     Discard Card x in Hand', 2,4,18)
        gametext_display('Space                                    Draw a card',2,3,18)
        gametext_display('s                           Show last played card',2,2.3,18)
        pygame.display.update()
        #action for help button, displays back button to main menu and rule button to rule screen and keybinds

def rulescreen():
    add_screen()
    startup = True
    while startup:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        back_button = createbutton('BACK',50,450,100,40,white, orange,help_screen)
        gametext_display("Rules: The rules of uno are simple.", 3.5,12,20)
        gametext_display("Your aim is to get rid of your cards before your opponent.", 2.3,9,20)
        gametext_display("Start the game by pressing the TAB button",3.3,7,20)
        gametext_display("Press the numbers keys to discard a card, e.g. 3 will discard your third card", 2,6,20)
        gametext_display("If you can't match the colour or number of the card on the pile, press SPACE",2,5,20)
        gametext_display("to draw another card",4.5,4.5,20)
        gametext_display("if you play a wrong card, a draw will be drawn for you", 3,4,20)
        gametext_display("Action Cards: Reverse- Reverses the turn order",2.5,3.5,20)
        gametext_display("Skip - skips the opponents turn", 3.5,3,20)
        gametext_display("+2- your opponent gets two extra cards", 2.5,2.5,20)
        pygame.display.update()
        #action for rule button, explains the rules of UNO

def singleplayer():
    pygame.mixer.music.load("Menumusic_2.mp3")
    pygame.mixer.music.play(-1)
    add_screen()
    play = True
    while play == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                deal_deck_selected()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                global down
                down = 0
                discard_card_selected()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                down = 1
                discard_card_selected()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                down = 2
                discard_card_selected()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                down = 3
                discard_card_selected()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                down = 4
                discard_card_selected()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_6:
                down = 5
                discard_card_selected()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_7:
                down = 6
                discard_card_selected()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_8:
                down = 7
                discard_card_selected()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_9:
                down = 8
                discard_card_selected()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                down = 9
                discard_card_selected()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                display_last_discarded()
                time.sleep(4)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                Player1.draw(deck, 1)
                Player1.showhand()
                gametext_display("You've drawn a card from the pile",2,5,15)
            #checks what number in the list of cards the user has selected to remove, and removes that card from their hand
            #pressing space draws a card for the user at any point in the game
            #pressing s displays the last card in play for 4 seconds as a reminder
                
            '''elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                global Uno_called
                UNO_called = True'''
        gametext_display('Player1', 12, 12, 15)
        gametext_display('Computer', 1.2, 12, 15)
        back_button = createbutton('BACK',300,500,200,40,white, orange,startup_menu) #back button to main menu
        width = (x/2.3) #location on screen
        height = (y/3) #location on screen
        deck_image(width,height) #blank UNO CARD image to represent pile
        pygame.display.update()
            


def empty_singleplayer_screen():
    add_screen()
    gametext_display('Player1', 12, 12, 15)
    gametext_display('Computer', 1.2, 12, 15)
    width = (x/2.3) #location on screen
    height = (y/3) #location on screen
    deck_image(width,height)
    #blank template for singleplayer screen, used after cards have been discarded to refresh view

def empty_multiplayer_screen():
    add_screen()
    gametext_display('Player1', 12, 12, 15)
    gametext_display('Player2', 1.2, 12, 15)
    width = (x/2.3)
    height = (y/3)
    deck_image(width,height)
    pygame.display.update()

        


def multiplayer():
    add_screen()
    startup = True
    while startup:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        back_button = createbutton('BACK',50,450,100,40,white, orange,startup_menu)
        #multiplayer_local_button = createbutton('Multiplayer Local',250,450,100,50,blue,orange,multiplayer_local)
        multiplayer_online_button = createbutton('Multiplayer Online',375,450,250,50,blue,orange,multiplayer_online)
        pygame.display.update()

def multiplayer_online():
    multiplayer = True
    while multiplayer == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        empty_multiplayer_screen()

def uno_gui():
    if login == True:
        startup_menu()
    else:
        print("User not logged in")
    #user must log in to play first

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
            uno_gui()
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
root = Tk()
root.title("Login Form")
Unologin(root)
root.mainloop()





