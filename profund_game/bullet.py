import pygame 

Screen_Width = 800
Screen_Height = 800*0.8

bullet_img = pygame.image.load('img/bullet/0.png')
scale = 15

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.image = pygame.transform.scale(bullet_img,(int(bullet_img.get_width()/scale),int(bullet_img.get_height()/scale)))
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.direction = direction
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image,True,False)
            
    def update(self):
        #move bullet
        self.rect.x += (self.direction*self.speed)
        #out of screen
        if self.rect.right < 0 or self.rect.left > Screen_Width:
            self.kill()
        