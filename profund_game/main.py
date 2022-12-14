#import lib and class
import pygame, sys, os, random ,csv, button, time
from pygame import mixer
from scoreboard import ScoreInput
from pygame.locals import *

#FPS
clock = pygame.time.Clock()
FPS = 60   

#init
mixer.init()
pygame.init()

#size screen
Screen_Width = 1280
Screen_Height = 720 

#setup window
screen = pygame.display.set_mode((Screen_Width,Screen_Height))
pygame.display.set_caption('The Soldier')
gameIcon = pygame.image.load('img/icon/65010895.png')
pygame.display.set_icon(gameIcon)

#variable
Gravity = 0.65

#variable map
SCROLL_THRESH = 250
ROWS = 16
COLS = 150
TILE_SIZE = Screen_Height // ROWS
TILE_TYPES = 27
screen_scroll = 0
bg_scroll = 0
MAX_LEVELS = 3
level = 1

#font
base_font = pygame.font.Font(None, 32)
base_font2 = pygame.font.Font(None, 56)


RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)

#load sound
pygame.mixer.music.load('audio/music2.mp3')
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1, 0.0, 5000)
item_fx = pygame.mixer.Sound('audio/item.wav')
item_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound('audio/jump.wav')
jump_fx.set_volume(0.5)
shot_fx = pygame.mixer.Sound('audio/shot.wav')
shot_fx.set_volume(0.5)


#load item
Health_img = pygame.image.load('img/Item/0.png').convert_alpha()
Damage_img = pygame.image.load('img/Item/1.png').convert_alpha()
Empty_img = pygame.image.load('img/Item/2.png').convert_alpha()
item_drops = {
    'Health' : Health_img,
    'Damage' : Damage_img,
    'Empty' : Empty_img,
}


class Item_Drop(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_drops[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x,y) 
            
    def draw(self):
        screen.blit(self.image,self.rect)
        
    def update(self):
        #check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            #check what kind of box it was
            if self.item_type == 'Health':
                player.health += 25
                item_fx.play()
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Damage':
                player.damage += 5
                item_fx.play()
            elif self.item_type == 'Empty':
                self.kill()
                enemy.kill()
            #delete the item box
            self.kill()
            enemy.kill()
            
item_boxes = {
    'Health' : Health_img,
    'Damage' : Damage_img,
}
class ItemBox(pygame.sprite.Sprite):
    def __init__(self, item_type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))


    def update(self):
        #scroll
        self.rect.x += screen_scroll
        #check if the player has picked up the box
        if pygame.sprite.collide_rect(self, player):
            #check what kind of box it was
            if self.item_type == 'Health':
                player.health += 25
                item_fx.play()
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'Damage':
                player.damage += 5
                item_fx.play()
            self.kill()

class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = base_font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        self.rect.x += screen_scroll
        self.rect.y -= 1
        # delete after a few seconds
        self.counter += 1
        if self.counter > 100:
            self.kill()
 

bullet_img = pygame.image.load('img/bullet/0.png').convert_alpha()
scale_bullet = 0.8
damage = 25
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = bullet_img
        self.image = pygame.transform.scale(bullet_img,(int(bullet_img.get_width()*scale_bullet),int(bullet_img.get_height()*scale_bullet)))
        self.rect = self.image.get_rect()
        self.direction = direction
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image,True,False) 
        self.rect.center = (x,y)
            
    def update(self):
        #move bullet
        if pause == False:
            self.rect.x += (self.direction*self.speed) + screen_scroll
        #out of screen
        if self.rect.right < 0 or self.rect.left > Screen_Width:
            self.kill()
        
        #check_collision_with_level
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        
        #check collision with characters
        if pygame.sprite.spritecollide(player, bullet_group, False):
            if player.alive:
                player.health -= 5*level
                player.temp_score -= 5*level
                self.kill()
                
        #test enemy
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy, bullet_group, False):
                if enemy.alive:
                    enemy.health -= player.damage
                    damage_text = DamageText(enemy.rect.centerx, enemy.rect.centery, str(player.damage), (255, 255, 255))
                    damage_text_group.add(damage_text)
                    self.kill()
                    
            
class Soldier(pygame.sprite.Sprite):
    
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = False
        self.flip = False
        self.shoot_cooldown = 0
        self.damage = damage
        self.health = 100
        self.max_health = self.health
        if char_type == 'enemy':
            self.health = 100*level
        else:
            self.health = 100
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()
        self.move_counter = 0
        self.vision = pygame.Rect(0, 0, 250, 10)
        self.idling = False
        self.idling_counter = 0
        self.ran = random.choice(['Health','Damage','Empty','Empty'])
        self.temp_score = 0
        
        #Animation
        animation_types = ['idle','run','jump','death']
        for animation in animation_types:
            temp_list = []
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
    def update(self):
        self.update_animation()
        self.check_alive()
        #update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
    def move(self, moving_left, moving_right):
        #reset movement
        screen_scroll = 0
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
        
        dy += self.vel_y
        
        if self.jump == True and self.in_air == False and dy == 0:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        
        #Gravity
        self.vel_y += Gravity
        
        #check_collision
        for tile in world.obstacle_list:
            #check_collision_x
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                  dx = 0
                  if self.char_type == enemy:
                      self.direction *= -1
                      self.move_counter = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                  if self.vel_y < 0:
                      self.vel_y = 0
                      dy = tile[1].bottom - self.rect.top
                  elif self.vel_y >= 0:
                      self.vel_y = 0
                      self.in_air = False
                      dy = tile[1].top - self.rect.bottom
        
        if pygame.sprite.spritecollide(self, water_group, False):
            self.health = 0
        
        level_complete = False    
        if pygame.sprite.spritecollide(self, exit_group, False):
            level_complete = True
        
        if self.rect.bottom > Screen_Height:
            self.health = 0
        
        
        if self.char_type == 'player':
            if self.rect.left + dx < 0 or self.rect.right + dx > Screen_Width:
                dx = 0
    
        #move rect   
        self.rect.x += dx
        self.rect.y += dy
        
        
        if self.char_type == 'player':
            if (self.rect.right > Screen_Width - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - Screen_Width) or (self.rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
                self.rect.x -= dx
                screen_scroll = -dx
        
            return screen_scroll, level_complete
        
        
        
    def shoot(self):
        if self.char_type == 'player':
            self.shoot_y = 0
        elif self.char_type == 'enemy':
            self.shoot_y = 20
        
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.75*self.rect.size[0]*self.direction), self.rect.centery, self.direction)
            bullet_group.add(bullet)
            shot_fx.play()
            
    def ai(self):
        if self.alive and player.alive and pause == False:
            
            if self.idling == False and random.randint(1, 120) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50
                self.vision.center = ((self.rect.centerx + 125 * self.direction) + screen_scroll, self.rect.centery)
                
            if self.vision.colliderect(player.rect):
                self.update_action(0)
                self.shoot()
                self.vision.center = ((self.rect.centerx + 125 * self.direction) + screen_scroll, self.rect.centery) 
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
                    self.vision.center = ((self.rect.centerx + 125 * self.direction) + screen_scroll, self.rect.centery)
                    
                    if self.move_counter > TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False
                
                if self.idling == True:
                    self.vision.center = ((self.rect.centerx + 125 * self.direction) + screen_scroll, self.rect.centery)
        
             
        self.rect.x += screen_scroll
            
            
        
    def update_animation(self):
        #update animation
        ANIMATION_COOLDOWN = 150
        
        self.image = self.animation_list[self.action][self.frame_index]     
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN and pause == False:
            self.update_time = pygame.time.get_ticks()
            if self.action != 3 or self.frame_index < len(self.animation_list[self.action])-1 :
                self.frame_index += 1
                if self.action == 3 and self.frame_index == 1 and self.char_type != 'player':
                    player.temp_score += 100
            if self.char_type != 'player' and player.alive == False:
                self.frame_index -= 1
        if self.frame_index >= len(self.animation_list[self.action])-2:
            if self.action == 3 and self.char_type != 'player':
                itemdrop = Item_Drop(self.ran,self.rect.centerx,self.rect.centery)
                itemdrop.draw()
                itemdrop.update()
            elif self.action == 3 and self.char_type == 'player':
                self.frame_index = len(self.animation_list[self.action]) - 1
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
        
img_list = []
for x in range(TILE_TYPES):
    img = pygame.image.load(f'img/tile/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE)) 
    img_list.append(img)        
class World():
    def __init__(self):
        self.obstacle_list = []
        
    def process_data(self, data):
        self.level_length = len(data[0])
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <=10:
                        water = Water(img, x * TILE_SIZE, y * TILE_SIZE)
                        water_group.add(water)
                    elif (tile >= 11 and tile <= 14) or tile >= 25:
                        decoration = Decoration(img, x * TILE_SIZE, y * TILE_SIZE)
                        decoration_group.add(decoration)
                    elif tile == 15:
                        player = Soldier('player',x * TILE_SIZE ,y * TILE_SIZE ,2 ,5)
                        health_bar = Health_Bar(10, 10, player.health, player.health)
                    elif tile == 16:
                        enemy = Soldier('enemy',x * TILE_SIZE ,y * TILE_SIZE ,0.8 ,2)
                        enemy_group.add(enemy)
                    elif tile == 17:
                        item_box = ItemBox('Damage', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 19:#create health box
                        item_box = ItemBox('Health', x * TILE_SIZE, y * TILE_SIZE)
                        item_box_group.add(item_box)
                    elif tile == 20:
                        exits = Exit(img, x * TILE_SIZE, y * TILE_SIZE)
                        exit_group.add(exits)
                    elif tile >= 21 and tile <= 24:
                        self.obstacle_list.append(tile_data)
                        

        return player, health_bar
    
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
            
            
class Decoration(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
    def update(self):
        self.rect.x += screen_scroll

            
            
class Water(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        
    def update(self):
        self.rect.x += screen_scroll
        
        
class Exit(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))                      
                        
    def update(self):
        self.rect.x += screen_scroll
        
def reset_level():
    enemy_group.empty()
    bullet_group.empty()
    decoration_group.empty()
    water_group.empty()
    exit_group.empty()
    damage_text_group.empty()
    item_box_group.empty()
    
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
                   
    return data          

start_img = pygame.image.load('img/button/start_btn.png').convert_alpha()
exit_img = pygame.image.load('img/button/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('img/button/restart_btn.png').convert_alpha()
home_img = pygame.image.load('img/button/home_btn.png').convert_alpha()
score_board_img = pygame.image.load('img/button/score_board_btn.png').convert_alpha()
reset_img = pygame.image.load('img/button/reset_btn.png').convert_alpha()
resume_img = pygame.image.load('img/button/resume_btn.png').convert_alpha()
yes_img = pygame.image.load('img/button/yes_btn.png').convert_alpha()
no_img = pygame.image.load('img/button/no_btn.png').convert_alpha()


            
pine1_img = pygame.image.load('img/background/pine1.png').convert_alpha()
pine2_img = pygame.image.load('img/background/pine2.png').convert_alpha()
mountain_img = pygame.image.load('img/background/mountain.png').convert_alpha()
sky_img = pygame.image.load('img/background/sky_cloud.png').convert_alpha()
sky_img = pygame.transform.scale(sky_img,(int(sky_img.get_width()*2.5),int(sky_img.get_height()*2.5)))
def draw_bg():
    screen.fill('grey')
    screen.blit(sky_img, (0, 0))
    width = mountain_img.get_width()
    for x in range(5):
        screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, Screen_Height - mountain_img.get_height() - 300))
        screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, Screen_Height - pine1_img.get_height() - 150))
        screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, Screen_Height - pine2_img.get_height()))

def draw_score():
    text_score = base_font.render("SCORE : " + str(score + player.temp_score), True, (255, 255, 255))
    screen.blit(text_score, (1100,20))
    
def draw_name():
    screen.fill('GREY')
    
    text_name = base_font2.render("INPUT YOUR NAME", True, (255, 255, 255))
    screen.blit(text_name, (Screen_Width//2 - text_name.get_width()//2, 50))
    
    text_surface = base_font.render(player_name, True, (255, 255, 255))
    pygame.draw.rect(screen, 'WHITE', pygame.Rect(Screen_Width//2 - text_surface.get_width()//2-5, Screen_Height//2 - text_surface.get_height()//2-5, text_surface.get_width()+10, text_surface.get_height()+5),  2)
    screen.blit(text_surface,(Screen_Width//2 - text_surface.get_width()//2, Screen_Height//2 - text_surface.get_height()//2))

def draw_menu():
    
    text_name = base_font2.render("THE SOLDIER", True, (255, 255, 255))
    screen.blit(text_name, (Screen_Width//2 - text_name.get_width()//2, 50))
    
    text_surface = base_font.render("65010895 Yotsapat Punyaworapan", True, (255, 255, 255))
    screen.blit(text_surface,(Screen_Width - text_surface.get_width()-5, Screen_Height - text_surface.get_height()-5))    

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
        
        
sctxt =open("save/scorebar.txt",'r')
pltxt =open("save/player.txt",'r')
scin =sctxt.read()
plin =pltxt.read()
                
scorex =""
scorelist =[]
scindex =-1

playerx=""
playerlist =[]
plindex =-1

for x in scin:
    scindex +=1
    scorex += x
    if x =='\n' or scindex == len(scin)-1:
        scorelist.append(scorex)
        scorex= ""

for x in plin:
    plindex +=1
    playerx += x
    if x =='\n' or plindex == len(plin)-1:
        playerlist.append(playerx)
        playerx= ""
sctxt.close()
pltxt.close()   
tran = True   
        
        
        
class Score_Board():
    
    def read (self):
        sctxt =open("save/scorebar.txt",'r')
        pltxt =open("save/player.txt",'r')
        scin =sctxt.read()
        plin =pltxt.read()
            
        scorex =""
        scorelist =[]
        scindex =-1

        playerx=""
        playerlist =[]
        plindex =-1

        for x in scin:
            scindex +=1
            scorex += x
            if x =='\n' or scindex == len(scin)-1:
                scorelist.append(scorex)
                scorex= ""

        for x in plin:
            plindex +=1
            playerx += x
            if x =='\n' or plindex == len(plin)-1:
                playerlist.append(playerx)
                playerx= ""

        self.playername_first = ScoreInput(screen,"1. "+playerlist[0],(0,0,0),20,150,3)
        self.playername_second = ScoreInput(screen,"2. "+playerlist[1],(0,0,0),20,250,3)
        self.playername_third = ScoreInput(screen,"3. "+playerlist[2],(0,0,0),20,350,3)
        self.playername_fourth = ScoreInput(screen,"4. "+playerlist[3],(0,0,0),20,450,3)
        self.playername_fifth = ScoreInput(screen,"5. "+playerlist[4],(0,0,0),20,550,3)
        
        self.score_first = ScoreInput(screen,scorelist[0],(0,0,0),500,150,3)
        self.score_second = ScoreInput(screen,scorelist[1],(0,0,0),500,250,3)
        self.score_third = ScoreInput(screen,scorelist[2],(0,0,0),500,350,3)
        self.score_fourth = ScoreInput(screen,scorelist[3],(0,0,0),500,450,3)
        self.score_fifth = ScoreInput(screen,scorelist[4],(0,0,0),500,550,3)

        sctxt.close()
        pltxt.close()
    def display_score(self):
        self.read()
        self.playername_first.draw()
        self.playername_second.draw()
        self.playername_third.draw()
        self.playername_fourth.draw()
        self.playername_fifth.draw()
        self.score_first.draw()
        self.score_second.draw()
        self.score_third.draw()
        self.score_fourth.draw()
        self.score_fifth.draw()
    def run(self):
        screen.fill('GREY')
        self.display_score() 
        


moving_left = False
moving_right = False
shoot = False

 
start_button = button.Button(Screen_Width //  2 - 96, Screen_Height // 2 - 150, start_img, 1.5)
exit_button = button.Button(Screen_Width //  2 - 96, Screen_Height // 2 + 150, exit_img, 1.5)
restart_button = button.Button(Screen_Width //  2 - 96, Screen_Height // 2 - 25, restart_img, 1.5)
home_button1 = button.Button(Screen_Width //  2 - 96, Screen_Height // 2 + 75, home_img, 1.5)
restart_button1 = button.Button(Screen_Width //  2 - 96, Screen_Height // 2 -75, restart_img, 1.5)
home_button = button.Button(Screen_Width - 292, Screen_Height // 2 - 25, home_img, 1.5)
score_board_button = button.Button(Screen_Width //  2 - 96, Screen_Height // 2 + 50, score_board_img, 1.5)
reset_button = button.Button(Screen_Width //  2 - 96, Screen_Height // 2 - 50, reset_img, 1.5)
resume_button = button.Button(Screen_Width //  2 - 96, Screen_Height // 2 - 125, resume_img, 1.5)
yes_button = button.Button(Screen_Width //  2 - 96, Screen_Height // 2 - 75, yes_img, 1.5)
no_button = button.Button(Screen_Width //  2 - 96, Screen_Height // 2 + 25, no_img, 1.5)
home_button2 = button.Button(Screen_Width //  2 - 96, Screen_Height // 2 + 75, home_img, 1.5)


damage_text_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
item_box_group = pygame.sprite.Group()



world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
    
    
def Resetmap():
    with open(f'map/level{level}_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x, row in enumerate(reader):
            for y, tile in enumerate(row):
                world_data[x][y] = int(tile)

Resetmap()
world = World()
player, health_bar = world.process_data(world_data)
    

player_name = ''
player_name_confirm = False
pause = False
start_game = False
reset_check = False
score_board_show = False
score_board = Score_Board()
score = 0
temp_damage = player.damage

run = True 
while run :
    
    if start_game == False:
        pause = False
        screen.fill('GREY')
        draw_menu()
        if reset_check == False:
            if start_button.draw(screen):
                start_game = True
                time.sleep(0.1)
            if reset_button.draw(screen):
                reset_check = True
                time.sleep(0.1)
            if score_board_button.draw(screen):
                score_board_show = True
                time.sleep(0.1)
            if exit_button.draw(screen):
                run = False
                time.sleep(0.1)
        elif reset_check:
            screen.fill('GREY')
            if yes_button.draw(screen):
                level = 1
                score = 0
                player.temp_score = 0
                player_name_confirm = False
                player_name = ''
                world_data = reset_level()
                Resetmap()
                world = World()
                player, health_bar = world.process_data(world_data)
                reset_check = False
                time.sleep(0.1) 
            if no_button.draw(screen):
                reset_check = False
                time.sleep(0.1)
        if score_board_show == True and reset_check == False:
            score_board.run()
            if home_button.draw(screen):
                    score_board_show = False
                    time.sleep(0.1)
            
                
    else:
        if player_name_confirm:
            draw_bg()
            world.draw()
            health_bar.draw(player.health)
            draw_score()
            
            player.draw()
            player.update()
            
            for enemy in enemy_group:
                enemy.ai()
                enemy.draw()
                enemy.update()
            
            #update and draw group
            damage_text_group.update()
            bullet_group.update()
            decoration_group.update()
            water_group.update()
            exit_group.update()
            item_box_group.update()
            damage_text_group.draw(screen)
            bullet_group.draw(screen)
            decoration_group.draw(screen)
            water_group.draw(screen)
            exit_group.draw(screen)
            item_box_group.draw(screen)
            
            
            #update action
            if player.alive:
                if pause == False:
                    if shoot:
                        player.shoot()
                    if player.in_air:
                        player.update_action(2)
                    elif moving_left or moving_right:
                        player.update_action(1)
                    else:
                        player.update_action(0)
                    screen_scroll, level_complete = player.move(moving_left,moving_right)
                    bg_scroll -= screen_scroll
                    
                    if level_complete:
                        score += player.temp_score
                        player.temp_score = 0
                        temp_damage = player.damage
                        level += 1
                        bg_scroll = 0
                        world_data = reset_level()
                        if level <= MAX_LEVELS:
                            Resetmap()
                            world = World()
                            player, health_bar = world.process_data(world_data)
                            player.damage = temp_damage
                        if level > MAX_LEVELS:
                            start_game = False
                            for x in range(len(scorelist)) :
                                if score >= int(scorelist[x]) and tran == True :
                                    scorelist.insert(x,str(score)+'\n')
                                    scorelist.pop(len(scorelist)-1)
                                    playerlist.insert(x,player_name+'\n')
                                    playerlist.pop(len(playerlist)-1)
                                    tran = False
                            plsend = ""
                            scsend = ""
                            for i in playerlist:
                                plsend += i
                            for i in scorelist:
                                scsend += i
                                
                            sctxt = open("save/scorebar.txt",'w') 
                            pltxt = open("save/player.txt",'w')
                            sctxt.write(scsend)
                            pltxt.write(plsend)
                            sctxt.close()
                            pltxt.close()
                            score_board_show = True
                            level = 1
                            score = 0
                            player.temp_score = 0
                            player_name_confirm = False
                            player_name = ''
                            world_data = reset_level()
                            Resetmap()
                            world = World()
                            player, health_bar = world.process_data(world_data)
                            if home_button.draw(screen):
                                score_board_show = False
                                time.sleep(0.1)
                else:
                    screen_scroll = 0
                    if restart_button.draw(screen):
                        bg_scroll = 0
                        world_data = reset_level()
                        with open(f'map/level{level}_data.csv', newline = '') as csvfile:
                            reader = csv.reader(csvfile, delimiter=',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int (tile)
                        world = World()
                        player, health_bar = world.process_data(world_data)
                        player.damage = temp_damage
                        pause = False
                        time.sleep(0.1)
                    elif home_button2.draw(screen):
                        player.temp_score = 0
                        bg_scroll = 0
                        world_data = reset_level()
                        Resetmap()
                        world = World()
                        player, health_bar = world.process_data(world_data)
                        player.damage = temp_damage
                        start_game = False
                        time.sleep(0.1)

                    
                    elif resume_button.draw(screen):
                        pause = False
                
            else:
                screen_scroll = 0
                if restart_button1.draw(screen):
                    bg_scroll = 0
                    world_data = reset_level()
                    player.temp_score = 0
                    Resetmap()
                    world = World()
                    player, health_bar = world.process_data(world_data)
                    player.damage = temp_damage
                    time.sleep(0.1)
                    
                elif home_button1.draw(screen):
                    player.temp_score = 0
                    bg_scroll = 0
                    world_data = reset_level()
                    Resetmap()
                    world = World()
                    player, health_bar = world.process_data(world_data)
                    player.damage = temp_damage
                    start_game = False
                    time.sleep(0.1)
                    
        else:
            pause = False
            draw_name()
            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif len(player_name) <= 20 and event.key != pygame.K_RETURN:
                        player_name += event.unicode
                    if event.key == pygame.K_RETURN and len(player_name) >= 1:
                        player_name_confirm = True
                        
                        
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_a:
                moving_left = True
            if event.key == K_d:
                moving_right = True
            if event.key == K_w and player.alive and player.in_air == False and start_game:
                jump_fx.play()
                player.jump = True
            if event.key == K_SPACE:
                shoot = True
            if event.key == K_ESCAPE:
                pause = True
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
