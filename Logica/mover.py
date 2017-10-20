import pygame
from GUI import Fundo


def notas():
    x1 = 110
    x2 = 80
    y1 = 10
    y2 = 80
    move = 0.6
    n1 =pygame.draw.rect(xd.screen,xd.BLACK,(x1,y1,x2,y2))
    pygame.display.flip
    while x1 <= 410:
        while y1<=800:
            n1 = pygame.draw.rect(xd.screen,xd.BLACK,(x1,y1,x2,y2))
            if x1>=210 and x1<= 410:
                n2 =pygame.draw.rect(xd.screen,xd.BLACK,(x1-100,y1-200,x2,y2))
            pygame.display.flip()
            y1+=move
            xd.fundo()
        y1=10
        x1+=100
        y0=10
