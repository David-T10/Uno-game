import pygame

pygame.init() #initialises pygame
unoDisplay = pygame.display.set_mode((800, 600)) #creates a window with specified resolution (x,y)
pygame.display.set_caption('UNO') #sets window title
gameClock = pygame.time.Clock() #creates a clock that counts fps
unoCall = False #in game loop once set to true game ends (basically when someone's called UNO and wins
while not unoCall: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            unoCall = True 

        print(event) 
        
    pygame.display.update() 
    gameClock.tick(60) 

pygame.quit() #pygame specific command to uninitiate pygame
quit()


