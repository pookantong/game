
from operator import truediv
import pygame
import time

pygame.init()

#variable
display_width = 800
display_height = 600
lead_x = display_width/2
lead_x_change = 0
lead_y = display_height/2
lead_y_change = 0
vel = 20
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
width = 40
height = 60

#fps
clock = pygame.time.Clock()   
FPS=30

font = pygame.font.SysFont(None,25)
def message_to_screen(msg,color):
    screen_text = font.render(msg,True,color)
    gamedisplay.blit(screen_text,[display_width/2,display_height/2])
#set display
gamedisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Road to the LEGEND")

pygame.display.update()


def gameloop():
    lead_x = display_width/2
    lead_x_change = 0
    lead_y = display_height/2
    lead_y_change = 0
    gameexit = False
    gameover = False
    while not gameexit:
        
        while gameover == True:
            message_to_screen("Gameover, press c to play again or press q to quit",red)
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameexit = True
                        gameover = False
                    if event.key == pygame.K_c:
                        gameloop() 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#close win
                gameexit = True
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_a:
                    lead_x_change = -vel
                    lead_y_change = 0
                if event.key ==pygame.K_d:
                    lead_x_change = vel
                    lead_y_change = 0
                if event.key ==pygame.K_w:
                    lead_y_change = -vel
                    lead_x_change = 0
                if event.key ==pygame.K_s:
                    lead_y_change = vel
                    lead_x_change = 0
        
        if lead_x > display_width-width or lead_x<0 or lead_y > display_height-height or lead_y < 0: 
            lead_x_change=0
            lead_y_change=0
            gameover = True       
        
        #continue moving    
        lead_x += lead_x_change 
        lead_y += lead_y_change 
        
        gamedisplay.fill(white)#white bg
        pygame.draw.rect(gamedisplay,black,[lead_x,lead_y,width,height])#character
        
        pygame.display.update()
        #fps
        clock.tick(FPS)


    pygame.quit()
    quit()

gameloop()