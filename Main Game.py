import random
import pygame
import os
import time  
from tkinter import *
from tkinter import messagebox as ms
import sqlite3
from sys import exit

pygame.mixer.pre_init(44100,16,2,4096)
pygame.init() #initialises pygame

skipturn = False
reverseturn = False
Player1wins = False
Computerwins = False
global down
x = 800
y = 600
div_iwidth = 750
div_iheight = 550
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
orange = (255,165,0)
mouseposition = pygame.mouse.get_pos()


class Card:
    def __init__(self, suit, number):
        self.suit = suit
        vals = {10: "reverse", 11:"skip", 12:"+2"}
        if type(number) is int:
            if number < 10:
                self.number = str(number)
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



class Player:
    def __init__(self, name):
        self.hand = []
        self.name = name

    def draw(self, deck, x):
        for i in range(x):
            self.hand.append(deck.drawcard())
            #allows player draw multiple cards


    def showhand(self):
      print("{} Hand is: ".format(self.name))
      h=30
      for card in self.hand:
          #print(card)
          displayimage(card.image,div_iwidth,div_iheight-h)
          pygame.display.update()
          h=h+25
      if len(self.hand) == 1:
         global UNO_called
         while UNO_called == False:
            gamtext_display("Press U to call UNO", 2,4,15)
            print("call uno thing")
            #pygame.display.update()
            if UNO_called == True:
                gametext_display("UNO CALLED", 2,5, 15)
                break
         pygame.display.update()
        
      elif len(self.hand) == 0:
        Player1wins = True
        add_screen()
        gametext_display("Player1 won. Game Over", 2, 2, 40)
        pygame.mixer.music.load("winnermusic.mp3")
        pygame.mixer.music.play(-1)
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        os._exit(1)


    def discard(self):
      global down
      if len(self.hand) != 0:
        discard_card = self.hand[down]
        self.throwAway(discard_card)
        if discard_card.number == "+2":
            gametext_display("Computer Draws 2 more cards", 2, 4,15)
            pygame.display.update()
            Computer.draw(deck, 2)
        elif discard_card.number == "skip":
            global skipturn
            skipturn = True
            gametext_display("Computer's Turn Will Be Skipped Next Round", 2, 4,15)
            pygame.display.update()
        elif discard_card.number == "reverse":
            global reverseturn
            reverseturn = True
            gametext_display("Computer's Turn Will Be Reversed Next Round", 2,4,15)
            pygame.display.update()
        

    def throwAway(self, discard):
       for card in self.hand:
          if card == discard:
              self.hand.remove(card)
              maingamepile.append(card)
              
              

              
              
              
class AI(Player):
    def discard(self):
        lastcardplaced = maingamepile[-1]
        for i in range (len(self.hand)):
            ai_card = self.hand[i]
            if ai_card.suit == lastcardplaced.suit or ai_card.number == lastcardplaced.number: #checks if card the computer wants to discard is the same suit or number as the card the player first discarded
                print("computer discarded", ai_card)
                self.throwAway(ai_card)
                if ai_card.number == "+2":
                    gametext_display("Player1 Draws 2 more cards", 2, 5,15)
                    pygame.display.update()
                    Player1.draw(deck, 2)
                elif ai_card.number == "skip":
                    gametext_display("Player1's Turn Skipped", 2, 5,15)
                    pygame.display.update()
                    Computer.discard()
                elif ai_card.number == "reverse":
                    gametext_display("Player1's Turn Reversed", 2,5,15)
                    pygame.display.update()
                    Computer.discard() 
                break
            else:
                gametext_display("Computer draws a card", 2, 5, 15)
                Computer.draw(deck, 1)
                break
        
       

    def showhand(self):
        print("{}'s Hand is: ".format(self.name))
        h=30
        for card in self.hand:
            #print(card)
            displayimage(deckImg,div_iwidth-600,div_iheight-h)
            pygame.display.update()
            h=h+25
        if len(self.hand) == 0:
            Computerwins = True
            add_screen()
            gametext_display("Computer won. Game Over", 2, 2, 40)
            pygame.display.update()
            time.sleep(5)
            pygame.quit()
            os._exit(1)
        
deck = Deck()
maingamepile = []
Player1 = Player('Player1')
Computer = AI('Computer')

#GUI + EXTRA FUNCTION STUFF

def displayimage(image_name,div_iwidth, div_iheight):
    iwidth = x-div_iwidth
    iheight = y-div_iheight
    uno_window.blit(image_name, (iwidth,iheight))
    time.sleep(0.3)

def text_objects(text, font): #this function takes the rectangle and puts it over the whole of the text so it can be moved as one
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def gametext_display(text,divby_x,divby_y,fontsize):
    gametext = pygame.font.Font('freesansbold.ttf', fontsize)
    TextSurf,TextRect = text_objects(text, gametext)
    TextRect.center = ((x/divby_x) ,(y/divby_y))
    uno_window.blit(TextSurf, TextRect)

def deal_deck_selected():
        deck.shuffle()
        Player1.draw(deck, 3)
        Player1.showhand()
        Computer.draw(deck, 3)
        Computer.showhand()
        gametext_display('Player1 starts first, use the number keys to select a card',2,12,15)
        
                               
def display_last_discarded():
    lastcardplaced = maingamepile[-1]
    displayimage(lastcardplaced.image, div_iwidth-300, div_iheight-150)
    gametext_display("Last placed card is:", 2, 3.5, 15)
    pygame.display.update()

def discard_card_selected():
    global skipturn
    global reverseturn
    if Player1wins == False and Computerwins == False and skipturn == False and reverseturn == False:
        Player1.discard()
        Computer.discard()
        empty_singleplayer_screen()
        Player1.showhand()
        Computer.showhand()
        display_last_discarded()
        time.sleep(4)
    elif skipturn == True:
        Player1.discard()
        skipturn = False
    elif reverseturn == True:
        Player1.discard()
        reverseturn = False
    
    

def deck_image(width,height):
    global deckImg
    deckImg = pygame.image.load('deck_image.png')
    uno_window.blit(deckImg, (width,height))


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
    pygame.mixer.music.load("Menumusic.mp3")
    pygame.mixer.music.play(-1)
    startup = True
    while startup:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gametext_display('Welcome to UNO',2,2,50)
        singeplayer_button = createbutton('SINGLEPLAYER',50,450,160,50,green,orange,singleplayer)
        mutliplayer_button = createbutton('MULTILPLAYER',250,450,160,50,blue,orange,multiplayer)
        quit_button = createbutton('QUIT',450,450,100,50,red,orange,quitgame)
        help_button = createbutton('HELP', 600,450,100, 50, white, orange,help_screen)
        pygame.display.update()

def quitgame():
    pygame.quit()
    quit()
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
        gametext_display("Action Cards: Reverse- Reverses the turn order",2.5,3.5,20)
        gametext_display("Skip - skips the opponents turn", 3.5,3,20)
        gametext_display("+2- your opponent gets two extra cards", 2.5,2.5,20)
        pygame.display.update()

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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                global Uno_called
                UNO_called = True
        gametext_display('Player1', 12, 12, 15)
        gametext_display('Computer', 1.2, 12, 15)
        back_button = createbutton('BACK',300,500,200,40,white, orange,startup_menu)
        width = (x/2.3) #location on screen
        height = (y/3) #location on screen
        deck_image(width,height)
        pygame.display.update()
            


def empty_singleplayer_screen():
    add_screen()
    #display_last_discarded()
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
        back_button = createbutton('BACK',50,450,100,40,white, orange,startup_menu)
        #multiplayer_local_button = createbutton('Multiplayer Local',250,450,100,50,blue,orange,multiplayer_local)
        multiplayer_online_button = createbutton('Multiplayer Online',375,450,250,50,blue,orange,multiplayer_online)
        pygame.display.update()

def multiplayer_online():
    pass

def uno_gui():
    if login == True:
        startup_menu()
    else:
        print("User not logged in")

# make database and users (if not exists already) table at programme start up
with sqlite3.connect('uno_user_database.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT NOT NULL ,password TEX NOT NULL);')
db.commit()
db.close()

#login class for uno
class Unologin:
    def __init__(self,master):
    	# Window 
        self.master = master
        # Some Usefull variables
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        #Create Widgets
        self.widgets()

    #Login Function
    def login(self):
    	#Establish Connection
        with sqlite3.connect('uno_user_database.db') as db:
            c = db.cursor()

        #Find user If there is any take proper action
        find_user = ('SELECT * FROM users WHERE username = ? and password = ?')
        c.execute(find_user,[(self.username.get()),(self.password.get())])
        result = c.fetchall()
        if result:
            self.logf.pack_forget()
            self.head['text'] = self.username.get() + '\n Logged In'
            self.head['pady'] = 100
            self.head['padx'] = 100
        else:
            ms.showerror('Username Not Found.')
            
    def new_user(self):
    	#Establish Connection
        with sqlite3.connect('uno_user_database.db') as db:
            c = db.cursor()

        #Find Existing username if any take proper action
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


    

#create window and application object
root = Tk()
root.title("Login Form")
Unologin(root)
root.mainloop()





