import pygame, sys

clock = pygame.time.Clock()

from pygame.locals import *
pygame.init()

Win_size=(400,400)

screen = pygame.display.set_mode(Win_size, 0,32)

player_image = pygame.image.load('profund_game/player.png')
player_location = [50,50]
player_y_momentum = 0

player_rect = pygame.Rect(player_location[0]-10,player_location[1],player_image.get_width()-10,player_image.get_height())
test_rect = pygame.Rect(100,100,100,50)

movingleft = False 
movingright = False 


while True :
    screen.fill('black')
    screen.blit(player_image,player_location)
    
    if player_location[1] > Win_size[1]-player_image.get_height():
        player_y_momentum = -player_y_momentum
    else:
        player_y_momentum += 0.2    
    player_location[1] += player_y_momentum
    
    if movingleft == True:
        player_location[0] -= 4
    if movingright == True:
        player_location[0] += 4  
        
    player_rect.x = player_location[0]
    player_rect.y = player_location[1]
           
    if player_rect.colliderect(test_rect):
        pygame.draw.rect(screen,(255,0,0),test_rect)
    else :
        pygame.draw.rect(screen,(0,0,255),test_rect)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                movingleft = True 
            if event.key == K_RIGHT:
                movingright = True
        if event.type == KEYUP:
            if event.key == K_LEFT:
                movingleft = False 
            if event.key == K_RIGHT:
                movingright = False                 
    pygame.display.update()
    clock.tick(60)
