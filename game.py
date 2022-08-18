import pygame
# Initialize
pygame.init()
# Create the screen
screen = pygame.display.set_mode((1280,720))

Running = True
while Running:
    for event in pygame.event.get():
        if event.type == pygame.quit():
            runnung = False
