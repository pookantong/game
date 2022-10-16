import pygame, sys
from player import Soldier
from bullet import Bullet

clock = pygame.time.Clock()
FPS = 60

from pygame.locals import *
pygame.init()

Screen_Width = 800
Screen_Height = 800*0.8

screen = pygame.display.set_mode((Screen_Width,Screen_Height))
pygame.display.set_caption('The Soldier')


RED = (255,0,0)

def draw_bg():
    screen.fill('grey')
    pygame.draw.line(screen, RED, (0,300),(Screen_Width,300))


moving_left = False
moving_right = False
shoot = False


player = Soldier('player',200 ,200 ,2.5,5)


run = True 
while run :
    
    draw_bg()
    player.draw()
    player.update_animation()
    
    #update and draw group
    player.bullet_group.update()
    player.bullet_group.draw(screen)
    
    
    if player.alive:
        if shoot:
            player.shoot()
        if player.in_air:
            player.update_action(2)
        elif moving_left or moving_right:
            player.update_action(1)
        else:
            player.update_action(0)
            
    player.move(moving_left,moving_right) 
    
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_a:
                moving_left = True
            if event.key == K_d:
                moving_right = True
            if event.key == K_w and player.alive:
                player.jump = True
            if event.key == K_SPACE:
                shoot = True
        if event.type == pygame.KEYUP:
            if event.key == K_a:
                moving_left = False
            if event.key == K_d:
                moving_right = False
            if event.key == K_w and player.alive:
                player.jump = False
            if event.key == K_SPACE:
                shoot = False
            
                            
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
sys.exit()
