import pygame ,os


Gravity = 0.5
Screen_Width = 800
Screen_Height = 800*0.8

screen = pygame.display.set_mode((Screen_Width,Screen_Height))

bullet_group = pygame.sprite.Group()

class Soldier(pygame.sprite.Sprite):
    
    def __init__(self, char_type, x, y,scale,speed ):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        
        #Animation
        animation_types = ['idle','run','jump']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png')
                img = pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
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
            
        if self.jump == True and self.in_air == False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        
        #Gravity
        self.vel_y += Gravity
        if self.vel_y > 10:
            self.vel_y 
        dy += self.vel_y
        
        #check_collision_floor
        if self.rect.bottom + dy > 300:
            dy = 300 - self.rect.bottom
            self.in_air = False
        
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
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            
            
    def update_action(self, new_action):
        
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
            
        
    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False) ,self.rect)