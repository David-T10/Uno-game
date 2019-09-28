import pygame


pygame.init() #initialises pygame
x = 800
y = 600
white = (255,255,255)
black = (0,0,0)
green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
mouseposition = pygame.mouse.get_pos()

def add_screen():
    global uno_window
    uno_window = pygame.display.set_mode((x, y)) #creates a window with specified resolution (x,y)
    pygame.display.set_caption('Python UNO') #sets window title
    fps = pygame.time.Clock() #creates a clock that counts fps
    fps.tick(60)
def text_objects(text, font, colour): #this function takes the rectangle and puts it over the whole of the text so it can be moved as one
    textSurface = font.render(text, True, colour) 
    return textSurface, textSurface.get_rect()

def createbutton(button_name,x1,y2,w1,h2,colour):
    mouse = pygame.mouse.get_pos()
    button_font_size = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(button_name, button_font_size, colour)
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
        TextSurf, TextRect = text_objects('Welcome to UNO', titlefont, black) #referencing the surface and box around the text so it can be moved around
        TextRect.center = ((x/2) ,(y/2))
        uno_window.blit(TextSurf, TextRect)
        createbutton('SINGLEPLAYER',150,450,100,50,green)
        createbutton('MULTILPLAYER',370,450,100,50,blue)
        createbutton('QUIT',550,450,100,50,red)
        pygame.display.update()
        







