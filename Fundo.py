import pygame
#from Logica import mover

pygame.init()
def desenha_nota(x,y):
    pygame.draw.arc(screen, BLACK, (x,y,80,45), 2, 10, 3)
def movimento(posx,posy):
    posx = x
    posy = y
    posy+=5
def init():
    pass
def teclas():
    K_a when press 110,550 RED
    K_s
    K_d
    k_f
def pontos():
    if notay>500 and noty<600 and K_a.pressed:
        pontos+=50
    else:
        pontos-=50

screen = pygame.display.set_mode((600,600))
WHITE = (255,255,255)
BLACK = (0,0,0)
COR = (255,222,173)

pygame.display.set_caption("Guitar Hero 0.1")

done = False
clock = pygame.time.Clock()

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(WHITE)
    def fundo():
        pygame.draw.rect(screen, COR, (100,0,400,600))
        
        pygame.draw.arc(screen, BLACK, (110,550,80,45), 2, 10, 3)
        pygame.draw.arc(screen, BLACK, (210,550,80,45), 2, 10, 3)
        pygame.draw.arc(screen, BLACK, (310,550,80,45), 2, 10, 3)
        pygame.draw.arc(screen, BLACK, (410,550,80,45), 2, 10, 3)
        
        pygame.draw.line(screen, BLACK, [100, 100], [500, 100], 2)
        pygame.draw.line(screen, BLACK, [100, 200], [500, 200], 2)
        pygame.draw.line(screen, BLACK, [100, 300], [500, 300], 2)
        pygame.draw.line(screen, BLACK, [100, 400], [500, 400], 2)
        pygame.draw.line(screen, BLACK, [100, 540], [500, 540], 3)
        pygame.draw.line(screen, BLACK, [100, 597], [500, 597], 3)

        pygame.draw.line(screen, BLACK, [100, 0], [100, 600], 5)
        pygame.draw.line(screen, BLACK, [200, 0], [200, 600], 5)
        pygame.draw.line(screen, BLACK, [300, 0], [300, 600], 5)
        pygame.draw.line(screen, BLACK, [400, 0], [400, 600], 5)
        pygame.draw.line(screen, BLACK, [500, 0], [500, 600], 5)
    fundo()
    pygame.display.flip()
    #Fim fundo

    mover.notas()
    clock.tick(60)
pygame.quit()

