import pygame, sys, os, math


def rotate2d(pos,rad): x,y=pos; s,c=math.sin(rad),math.cos(rad); return x*c-y*s,x*s+y*c

def rotate3d(pos,rot):
    x,y,z = pos
    if rot[2]: x,y = rotate2d((x,y),rot[2])
    if rot[1]: z,x = rotate2d((z,x),rot[1])
    if rot[0]: y,z = rotate2d((y,z),rot[0])
    return x,y,z

def Texture(image,size=None):
    w,h = size if size else image.get_size(); texture = []
    for y in range(h): row=pygame.Surface((w,1)); row.blit(image,(0,-y)); texture+=[row]
    return texture

class Simulator:
    rotX,rotY = -18.5/180*math.pi,0; pos = [0,1.8,-1.2]

    top,bottom = 0.4,0.10
    buttonZ = (top+bottom)/3 # buttons z position
    range = 6 # length of guitar neck, texture at each square
    colors = (7,183,94),(165,70,62),(255,255,147),(0,142,197),(199,122,71) # green red yellow blue orange
    speed = 2/0.475 # hyper speed (has to be above 0) # 2 makes the bars cross every second, 2/0.475 makes them cross every 0.475 seconds
    f = 1/5,3/5,1/10 # constant fractions
    z = 0 # convayer belt position
    running = False # is the song playing?
    score = 0
    keys = [0,0,0,0,0] # state of guitar keys
    streak = 0 # notes hit in a row
    multiplier = 1 # multiplies points
    max_mult = 4 # highest multiplier
    min_mult = 1 # lowest multiplier (won't get any points on a 0 multiplier, obviously)
    mult_streak = 10 # amount of notes in streak to increment multiplier

    time = 0 # to keep track of time

    def __init__(self,window_size):
        self.w,self.h = window_size; self.cx,self.cy = self.w//2,self.h//2
        self.font = pygame.font.Font('C:/Windows/Fonts/Arial.ttf',20)
        self.load_texture('texture.png')
        self.load_song('song.txt','song.mp3')
        self.play_song()
        self.init_joysticks()

    def init_joysticks(self):
        J = pygame.joystick; J.quit(); J.init(); self.joysticks = []
        for i in range(J.get_count()): j = J.Joystick(i); j.init(); self.joysticks+=[j]

    def load_texture(self,dir):
        self.image = pygame.image.load(dir); size = self.image.get_size()
        self.texture = [Texture(self.image,size),size]
        self.fractions = [2*y/size[1] for y in range(size[1])]

    def play_song(self):
        pygame.mixer.music.play(0)
        self.running = True

    def load_song(self,notes,music):
        pygame.mixer.music.load(music)

        self.chords = open(notes).read().split('\n')[::-1] # flip the list so the notes are drawn from back to front
        for i in range(len(self.chords)):
            keys,time = eval(self.chords[i])
            self.chords[i] = [keys,self.buttonZ+time*self.speed]

    def events(self,event):
        mouse = pygame.mouse.get_pressed()
        if event.type == pygame.MOUSEMOTION and mouse[0]: self.rotY-=event.rel[0]/100; self.rotX-=event.rel[1]/100 # useful for setting camera rotation with mouse

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: self.rotX,self.rotY = -18.5/180*math.pi,0; self.pos = [0,1.8,-1.2]
            if event.key == pygame.K_2: self.rotX,self.rotY = -16/180*math.pi,0; self.pos = [0,1.2,-0.9]

        elif event.type == pygame.JOYHATMOTION:
            if event.joy == self.joysticks[0].get_id(): # only from pad 1
                x,y = self.joysticks[0].get_hat(event.hat) # state of hat
                if y: # if strummed up or down
                    if any(self.keys):
                        combo = [0,0,0,0,0]
                        for i in range(len(self.chords)):
                            t = self.chords[i][1]
                            if t<self.top and t>self.bottom: combo = tuple(self.chords[i][0]); break

                        if any(combo):
                            if self.keys==combo or (combo.count(1)==1 and self.keys[combo.index(1)] and not any(self.keys[combo.index(1)+1:])): # hit successful
                                del self.chords[i]
                                self.score+=50*self.multiplier
                                self.streak+=1
                            else: self.streak = 0

                    else: self.streak = 0 # strummed nothing

    def update(self,fs,key):
        self.time+=fs

        self.multiplier = min(self.streak//self.mult_streak+self.min_mult,self.max_mult) # update multiplier
        self.keys = tuple(self.joysticks[0].get_button(i) for i in (0,1,3,2,4)) if self.joysticks else (0,0,0,0,0)

        s = 0.1 # fly speed
        if key[pygame.K_e]: self.pos[1]+=s
        if key[pygame.K_q]: self.pos[1]-=s

        x,y = math.sin(self.rotY)*s,math.cos(self.rotY)*s
        if key[pygame.K_w]: self.pos[0]-=x; self.pos[2]+=y
        if key[pygame.K_s]: self.pos[0]+=x; self.pos[2]-=y
        if key[pygame.K_a]: self.pos[0]-=y; self.pos[2]-=x
        if key[pygame.K_d]: self.pos[0]+=y; self.pos[2]+=x


        for i in range(len(self.chords)):
            t = self.chords[i][1]
            if t<0: self.streak = 0

        if self.speed: # if there's speed, let's move.
            s = fs*self.speed
            self.z+=s
            for chord in self.chords: chord[1]-=s # move chords towards target

            if not self.running:
                self.speed-=fs*1.7 # slow down
                if self.speed<0.2: self.speed = 0 # slow enough, let's just stop...

        self.running = pygame.mixer.music.get_busy() # is the song still playing?

        if not self.joysticks: self.init_joysticks()

    def pos2d(self,x,z):
        X,Y,Z = self.pos
        x,y,z = rotate3d((x-X,-Y,z-Z),(self.rotX,self.rotY,0))
        f = 300/z if z>0 else 90000
        return int(self.cx+x*f),int(self.cy-y*f)

    def draw_textures(self,screen):
        t,(w,h) = self.texture; s = 2 # box size
        for Z in range(0,self.range,s):
            for y in range(h):
                f = self.fractions[y]
                z = (f+Z-self.z)%self.range
                a,b = self.pos2d(-1,z),self.pos2d(1,z) # left and right point of line (image to be drawn on)
                try: screen.blit(pygame.transform.scale(t[-y],(b[0]-a[0],s)),a) # not fixed for rotating cam left or right, only up and down so far
                except: pass # incase there's a problem

    def draw_strings(self,screen):
        for x in (-self.f[0],-self.f[1],self.f[0],self.f[1]): pygame.draw.line(screen,(0,255,0),self.pos2d(x,0),self.pos2d(x,self.range),2)

        for z in range(0,self.range,2):
            points = [self.pos2d(X,(Z-self.z)%self.range) for X,Z in ((-1,z),(1,z))]
            pygame.draw.line(screen,(0,128,0),points[0],points[1],8)

    def draw_border(self,screen):
        for x in (-1,1): pygame.draw.line(screen,(0,0,0),self.pos2d(x,0),self.pos2d(x,self.range),10)

    def draw_fret(self,screen,x,z,i=None,color=None):
        try:
            if z>self.range or z<-0.4: return
            pos = self.pos2d(x/2.5,z)
            a,b = self.pos2d(-self.f[2],z),self.pos2d(self.f[2],z)
            r = min(abs(a[0]-b[0]),100)
            X,Y,W,H = pos[0]-r,pos[1]-r,r*2,r*1.3
            rect = X+4,Y+4,W-8,H-8
            pygame.draw.ellipse(screen,(0,0,0),(X,Y,W,H))
            pygame.draw.ellipse(screen,color if color else self.colors[i if i else x+2],rect)
        except: pass

    def draw_notes(self,screen):
        t,b = self.top,self.bottom
        l = tuple(self.pos2d(x,z) for x,z in ((-1,t),(-1,b),(1,b),(1,t)))
        try: pygame.draw.polygon(screen,(0,0,0),l)
        except: pass # found problem

        for x in (-2,-1,0,1,2):
            i=x+2; c = self.colors[i]
            state = self.joysticks[0].get_button((0,1,3,2,4)[i]) if self.joysticks else False
            color = c if state else (c[0]//4,c[1]//4,c[2]//4)
            self.draw_fret(screen,x,self.buttonZ,i,color)

        for notes,time in self.chords:
            for x in (-2,-1,0,1,2):
                i=x+2
                if notes[i]:
                    collide = time<self.top and time>self.bottom
                    self.draw_fret(screen,x,time,i,(255,0,255) if collide else None)

    def draw_score(self,screen):
        screen.blit(self.font.render('Score: %d'%self.score,2,(0,255,0)),(20,200))
        screen.blit(self.font.render('Streak: %d'%self.streak,2,(0,255,0)),(20,230))
        screen.blit(self.font.render('Multiplier: %d'%self.multiplier,2,(0,255,0)),(20,260))
        screen.blit(self.font.render('Time: %.1f'%self.time,2,(0,255,0)),(20,290))

    def draw_cam_stats(self,screen):
        screen.blit(self.font.render('Position: X:%.2f Y:%.2f Z:%.2f'%tuple(self.pos),2,(0,255,0)),(20,30))
        screen.blit(self.font.render('Rotation: X:%.2f Y:%.2f'%(self.rotX*180/math.pi,self.rotY*180/math.pi),2,(0,255,0)),(20,70))

    def draw(self,screen):
        self.draw_textures(screen)
        self.draw_strings(screen)
        self.draw_border(screen)
        self.draw_notes(screen)
        self.draw_score(screen)
        self.draw_cam_stats(screen)


def main():
    pygame.init()
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.display.set_caption('Guitar Hero')
    w,h = 800,450; cx,cy = w//2,h//2
    screen = pygame.display.set_mode((w,h))
    fpsclock = pygame.time.Clock(); fps = 60
    program = Simulator((w,h))
    bg = pygame.transform.scale(pygame.image.load('background.jpg'),(w+cx,h+cy))

    while True:
        fs = fpsclock.tick(fps)/1000

        screen.fill((128,128,255))
        screen.blit(bg,(-cx//2,-cy//2-40))
        program.draw(screen)
        pygame.display.flip()

        key = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if key[pygame.K_LALT] and event.type == pygame.KEYDOWN and event.key == pygame.K_F4: pygame.quit(); sys.exit()
            program.events(event)

        program.update(fs,key)


if __name__ == '__main__':
    main()



