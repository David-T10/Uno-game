import pygame


pygame.init() #initialises pygame
x = 800
y = 600
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
orange = (255,165,0)
mouseposition = pygame.mouse.get_pos()

def add_screen():
    global uno_window
    uno_window = pygame.display.set_mode((x, y)) #creates a window with specified resolution (x,y)
    pygame.display.set_caption('Python UNO') #sets window title
    fps = pygame.time.Clock() #creates a clock that counts fps
    fps.tick(60)
    uno_window.fill(white)
    card_image = pygame.image.load('uno_card.png')
    pygame.display.update()
    
def text_objects(text, font): #this function takes the rectangle and puts it over the whole of the text so it can be moved as one
    textSurface = font.render(text, True, black) 
    return textSurface, textSurface.get_rect()

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
        uno_window.fill(white)
        titlefont = pygame.font.Font('freesansbold.ttf', 50)
        TextSurf, TextRect = text_objects('Welcome to UNO', titlefont) #referencing the surface and box around the text so it can be moved around
        TextRect.center = ((x/2) ,(y/2))
        uno_window.blit(TextSurf, TextRect)
        singeplayer_button = createbutton('SINGLEPLAYER',150,450,100,50,green,orange,add_screen)
        mutliplayer_button = createbutton('MULTILPLAYER',370,450,100,50,blue,orange,add_screen)
        quit_button = createbutton('QUIT',550,450,100,50,red,orange,quitgame)
        pygame.display.update()

def quitgame():
    pygame.quit()
    quit()

def card_image(width,height):
    uno_window.blit(card_image, (width,height))
    width = (x * 0.25)
    height = (y * 0.25)

def maingame_loop():
        startup_menu()


maingame_loop()
        







