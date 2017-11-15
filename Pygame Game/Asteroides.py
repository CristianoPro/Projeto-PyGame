import pygame
import sys, os
from pygame.locals import *
import random


pygame.init() 
clock = pygame.time.Clock()
screen = pygame.display.set_mode((600,600))



bg = pygame.image.load(os.path.join("images", "fundo.png"))

clock = pygame.time.Clock

asteroide = pygame.image.load(os.path.join("images","asteroide.png"))
nave = pygame.image.load(os.path.join("images", "nave.png"))

nave_top = screen.get_height() - nave.get_height() - 10
nave_left = screen.get_width()/2 - nave.get_width()/2

screen.blit(nave, (nave_left,nave_top))

shot = pygame.image.load(os.path.join("images", "tiro.png"))
ast = pygame.image.load(os.path.join("images","asteroide.png"))
shoot_y = 600
shoot_x = 0

pygame.display.set_caption('Asteroids')

x = 300
y = 300

x_rand = random.randint(20,530)
y_ast = 0


while True:
    screen.blit(bg, (0,0))

    screen.blit(nave, (x-nave.get_width()/2, nave_top))
    screen.blit(shot,(shoot_x, shoot_y))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                shoot_y = 530
                shoot_x = x
                
    if shoot_y>-10:
        screen.blit(shot,(shoot_x,shoot_y))
        shoot_y -=10
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            x -= 2
        if event.key == pygame.K_RIGHT:
            x +=2
        
        screen.blit(ast,(x_rand,y_ast))
    if y_ast <= 600:
        y_ast+=10
    else:
        y_ast = 0
    pygame.display.update()
    if y_ast == 0:
        x_rand = random.randint(20,530)  

