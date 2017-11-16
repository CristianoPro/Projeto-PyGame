#Guilherme Mangili Vilas Boas 31719155
#Fernando Brandão Moredo 31739601
#Henrique Magno 31731090
#Cristiano Souza de Oliveira 41612590
#Git https://github.com/CristianoPro/Projeto-PyGame

import pygame
import random
from pygame.locals import *
pygame.init()
pygame.mixer.music.load('Legado 47- Fantasmas e Monstros.mp3')
pygame.mixer.music.play()

##COLOURS
BLACK    = (   0,   0,   0) ; WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0) ; RED      = ( 255,   0,   0)

import ctypes

messageBox = ctypes.windll.user32.MessageBoxW

messageBox(None,"Make sure your sound is on, and enter your name so your score is saved","Double Hero",0x40 | 0x0)

##Screen Size
size    = (467, 700)  

##HIGHSCORES FILE
file = open("highscores.txt", "r")
lineList = file.readlines()
file.close()

##BOOLEANS
done    = False # Loop until the close clicked
intro   = False # Loop until intro is over
running = True # another boolean for a loop to blit images
screenopened = False
introm = True
namein = False

#Clock for FPS
clock   = pygame.time.Clock() #Load pygame clock for refresh rate

##Number variables
score = 0 
lives = 3
speed = 0
drawcircle = 1   
nCircles = 0
pos2 = 20

##IMAGES
hat = pygame.image.load('hat.png')
img = pygame.image.load('background1.png')
imgbackground = pygame.image.load('background.png')

##MUSIC
intromusic = pygame.mixer.Sound("intromusic.wav")
intromusic.set_volume(0.1)
beepSound = pygame.mixer.Sound("beep-01a.wav")
beepSound.set_volume(0.1)

myfont = pygame.font.SysFont("arial", 30)

while not intro:
    if namein == False:
        name = input("Enter your name: ")
        namein = True
        
    if screenopened == False:
        screen = pygame.display.set_mode(size)
        pygame.display.flip()
        pygame.display.set_caption("Collect the Circles | Score 0")
        screenopened= True
        
    highscore = myfont.render(lineList[len(lineList)-1], 1, WHITE)
    screen.blit(highscore, (200, 656))
    
    ##SCORE TEXT
    screen.blit(img,(0,0))
    prev = myfont.render("Previous score: ", 1, WHITE)
    highscore = myfont.render(lineList[len(lineList)-1], 1, WHITE)
    screen.blit(highscore, (300, 656))
    screen.blit(prev, (100, 656))

    ##EASY HARD BUTTONS
    rect1 = pygame.draw.rect(screen,WHITE, (60,350,140,100),0)
    rect2 = pygame.draw.rect(screen,WHITE, (280,350,140,100),0)
    imgeasy = pygame.image.load('easy.png')
    screen.blit(imgeasy,(60,360))
    imghard = pygame.image.load('hard.png')
    screen.blit(imghard,(280,360))

    ##MUSIC
    if introm == True:
        intromusic.play()
        introm = False
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If user clicked close
            intro = True # Flag that we are done so we exit this loop
            done = True
            intromusic.stop()
            
        ##CLICKING EITHER EASY OR HARD
        position = pygame.mouse.get_pos()
        x = position[0]
        y = position[1]
        if pygame.mouse.get_pressed()[0]:
            is_insidespeed1 = rect1.collidepoint(x,y)
            is_insidespeed2 = rect2.collidepoint(x,y)
            if is_insidespeed1:
                speed = 1
                rect1 = pygame.draw.rect(screen,GREEN, (100,350,100,100),0)
                intro = True
                pygame.display.flip()
                intromusic.stop()
            if is_insidespeed2:
                speed = 3
                rect2 = pygame.draw.rect(screen,GREEN, (250,350,100,100),0)
                intro = True
                pygame.display.flip()
                intromusic.stop()

            
while not done:


    ##WHERE CIRCLE IS DROPPED
    pos = random.randint(1,4)
    if nCircles == 0:
        pos2 = 20
        if pos == 1:
            pos1 = 77
            COLOUR = RED
            nCircles = 1
            drawcircle = 1
        if pos == 2:
            pos1 = 153
            COLOUR = GREEN
            nCircles = 1
            drawcircle = 1
        if pos == 3:
            pos1 = 230
            COLOUR = BLACK
            nCircles = 1
            drawcircle = 1
        if pos == 4:
            pos1 = 306
            COLOUR = RED
            nCircles = 1
            drawcircle = 1

    ##LIVES AND BACKGROUND
    if running == True:
        screen.blit(imgbackground,(0,0)) 
        pos2 = pos2 + speed
    if lives == 3:
        screen.blit(hat,(400,140))
        screen.blit(hat,(400,200))
        screen.blit(hat,(400,260))
    if lives == 2:
        screen.blit(hat,(400,140))
        screen.blit(hat,(400,200))
    if lives == 1:
        screen.blit(hat,(400,140))
    if drawcircle == 1:
        myCircle = pygame.draw.circle(screen,COLOUR,(pos1,pos2), 9,0)


    ##Printing live score to the screen
    score = str(score)
    myfont = pygame.font.SysFont("arial", 30)
    scoretext = myfont.render(score, 1, (37,222,255))
    screen.blit(scoretext, (200, 656))
    pygame.display.flip()

    ##If 0 Lives game is over
    if lives == 0:
        done = True # Flag that we are done so we exit this loop

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        score = int(score)
        if pos2 >= 660:
            lives = lives - 1
            drawcircle = 0
            nCircles = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                is_inside = myCircle.collidepoint(77,595)
                if is_inside:
                    drawcircle = 0
                    nCircles = 0
                    score = score + 1
                    beepSound.play()
                    pygame.display.set_caption("Collect the Circles | Score " + str(score))
                else:
                    lives = lives - 1
                    drawcircle = 0
                    nCircles = 0
            if event.key == pygame.K_2:
                is_inside = myCircle.collidepoint(153,595)
                if is_inside:
                    drawcircle = 0
                    nCircles = 0
                    score = score + 1
                    beepSound.play()
                    pygame.display.set_caption("Collect the Circles | Score " + str(score))
                else:
                    lives = lives - 1
                    drawcircle = 0
                    nCircles = 0
            if event.key == pygame.K_3:
                is_inside = myCircle.collidepoint(230,595)
                if is_inside:
                    drawcircle = 0
                    nCircles = 0
                    score = score + 1
                    beepSound.play()
                    pygame.display.set_caption("Collect the Circles | Score " + str(score))
                else:
                    lives = lives - 1
                    drawcircle = 0
                    nCircles = 0
            if event.key == pygame.K_4:
                is_inside = myCircle.collidepoint(306,595)
                if is_inside:
                    drawcircle = 0
                    nCircles = 0
                    score = score + 1
                    beepSound.play()
                    pygame.display.set_caption("Collect the Circles | Score " + str(score))
                else:
                    lives = lives - 1
                    drawcircle = 0
                    nCircles = 0


##SAVING THE SCORE                    
file = open("highscores.txt", "a")
score = str(score)
file.write(name)
file.write(":  ")
file.write(score)
file.write("\n")
file.close()
pygame.quit()
