import pygame, sys, os, random

clock = pygame.time.Clock()
FPS = 60   

from pygame.locals import *
pygame.init()

Screen_Width = 800
Screen_Height = 800*0.8 

screen = pygame.display.set_mode((Screen_Width,Screen_Height))
pygame.display.set_caption('The Soldier')


Gravity = 0.5
TILE_SIZE = 40


RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
Health_img = pygame.image.load('img/Item/0.png')
Damage_img = pygame.image.load('img/Item/1.png')
item_drops = {
    'Health' : Health_img,
    'Damage' : Damage_img,
}

class Item_Drop(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_drops[self.item_type]
        self.rect = self.image.get_rect()
        for enemy in enemy_group:
            self.rect.midtop = (x,y) 
    def draw(self):
        screen.blit(self.image,self.rect)
    

bullet_img = pygame.image.load('img/bullet/0.png')
scale_bullet = 3/4
damage = 100
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.image = pygame.transform.scale(bullet_img,(int(bullet_img.get_width()/scale_bullet),int(bullet_img.get_height()/scale_bullet)))
        self.rect = self.image.get_rect()
        self.pos_bull = 10
        self.direction = direction
        self.damage = damage
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image,True,False)
            self.pos_bull =  self.pos_bull * -1 
        self.rect.center = (x,y+20)
            
    def update(self):
        #move bullet
        self.rect.x += (self.direction*self.speed)
        #out of screen
        if self.rect.right < 0 or self.rect.left > Screen_Width:
            self.kill()
        #check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5
                self.kill()
        #test enemy
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= self.damage
                    self.kill()
            
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
        self.shoot_cooldown = 0
        self.health = 100
        self.max_health = self.health
        self.health = 100
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 200, 20)
        self.idling = False
        self.idling_counter = 0
        self.ran = random.choice(['Health','Damage'])
        
        #Animation
        animation_types = ['idle','run','jump','death']
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
        
    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
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
        
        #check_collision_walls
        if self.rect.left + dx < 0 or self.rect.right + dx > Screen_Width:
            self.direction * self.speed
        
        #move rect   
        self.rect.x += dx
        self.rect.y += dy
        
    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.7*self.rect.size[0]*self.direction),self.rect.centery, self.direction)
            bullet_group.add(bullet)
            
    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and random.randint(1, 200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50
                
            if self.vision.colliderect(player.rect):
                self.update_action(0)
                self.shoot() 
            else: 
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left = not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
            
            
        
    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 150
        
        self.image = self.animation_list[self.action][self.frame_index]     
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            if self.action != 3 or self.frame_index < len(self.animation_list[self.action])-1:
                self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                itemdrop = Item_Drop(self.ran,self.rect.centerx,self.rect.centery)
                itemdrop.draw()
            else:
                self.frame_index = 0
            
            
    def update_action(self, new_action):
        
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)
            
        
    def draw(self):
        screen.blit(pygame.transform.flip(self.image,self.flip,False) ,self.rect)          
            

def draw_bg():
    screen.fill('grey')
    pygame.draw.line(screen, RED, (0,300),(Screen_Width,300))

class Health_Bar():
    def __init__(self, x, y, health, max_health):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        
    def draw(self, health):
        
        self.health = health
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, BLACK, (self.x-2, self.y-2, 154, 24))
        pygame.draw.rect(screen, RED, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, GREEN, (self.x, self.y, 150 * ratio, 20))


moving_left = False
moving_right = False
shoot = False

enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()


player = Soldier('player',200 ,200 ,1 ,5)
health_bar = Health_Bar(10, 10, player.health, player.health)

enemy = Soldier('player',400 ,250 ,1 ,2 )
enemy2 = Soldier('player',600 ,250 ,1 ,2)
enemy_group.add(enemy)
enemy_group.add(enemy2)

run = True 
while run :
    
    draw_bg()
    health_bar.draw(player.health)
    
    player.draw()
    player.update()
    for enemy in enemy_group:
        enemy.ai()
        enemy.draw()
        enemy.update()
    
    #update and draw group
    bullet_group.update()
    bullet_group.draw(screen)
    
    
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
