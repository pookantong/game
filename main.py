import pygame

pygame.init()

#screen resolution
screen = pygame.display.set_mode((800,600))

#Title and Icon
pygame.display.set_caption("Test system")
Icon = pygame.image.load('')

#Game loop ไม่ให้หยุดทำงาน
running = True
while running :
    for event in pygame.event.get():
        if event.type == pygame.quit:
            running = False
    