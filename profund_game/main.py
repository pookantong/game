import pygame, sys

clock = pygame.time.Clock()
FPS = 60

from pygame.locals import *
pygame.init()

Screen_Width = 800
Screen_Height = 800*0.8

screen = pygame.display.set_mode((Screen_Width,Screen_Height))
pygame.display.set_caption('The Soldier')


class Soldier(pygame.sprite.Sprite):
    
    def __init__(self, char_type, x, y,scale,speed ):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        tmp_list = []
        for i in range(7):
            img = pygame.image.load(f'img/{self.char_type}/run/{i}.png')
            img = pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
            tmp_list.append(img)
        for i in range(3):
            img = pygame.image.load(f'img/{self.char_type}/run/{i}.png')
            img = pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
            tmp_list.append(img)
        self.animation_list.append(tmp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        
    def move(self, moving_left, moving_right):
        
        #reset movement
        dx = 0
        dy = 0
        
        if moving_left:
            dx =  -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dx =  self.speed
            self.flip = False
            self.direction = 1
        
        #move rect   
        self.rect.x += dx
        self.rect.y += dy
        
    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 100
        
        self.image = self.animation_list[self.action][self.frame_index]       
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
            
        
    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False) ,self.rect)


moving_left = False
moving_right = False
player = Soldier('player',200 ,200 ,2.5,5)


run = True 
while run :
    
    screen.fill('grey')
    player.draw()
    player.update_animation()
    player.move(moving_left,moving_right)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_a:
                moving_left = True
            if event.key == K_d:
                moving_right = True
        if event.type == pygame.KEYUP:
            if event.key == K_a:
                moving_left = False
            if event.key == K_d:
                moving_right = False
            
                            
    pygame.display.update()
    clock.tick(FPS)
pygame.quit()
sys.exit()
