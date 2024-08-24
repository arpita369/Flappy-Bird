import pygame
import random
import time as t
from pygame import mixer


#initialize the pygame 
pygame.init()


#clock
FPS = 200 #frames per second
fpsclock = pygame.time.Clock()


#make the screen
screen = pygame.display.set_mode(size=(600,600)) 


#caption and icon
pygame.display.set_caption("FLAPPY BIRD")
icon = pygame.image.load("FP_BIRD_Icon.png")
pygame.display.set_icon(icon)


#background
background = pygame.image.load("FP_BIRD_Background.jpg").convert_alpha()
background = pygame.transform.scale(background, (600,600))


#tree1
bgtree1 = pygame.image.load("FP_BIRD_Trees.png")
bgtree1 = pygame.transform.scale(bgtree1, (700,300))
bgtree1X = -100
bgtree1Y = 200
bgtree1X_change = 100

def tree1(x,y):
    screen.blit(bgtree1,(x,y))


#tree2
bgtree2 = pygame.image.load("FP_BIRD_Trees.png")
bgtree2 = pygame.transform.scale(bgtree2, (700,300))
bgtree2X = 300
bgtree2Y = 200
bgtree2X_change = 100

def tree2(x,y):
    screen.blit(bgtree2,(x,y))


#road
bgroad = pygame.image.load("FP_BIRD_Road.png")
bgroad = pygame.transform.scale(bgroad, (900,200))
bgroadX = 0
bgroadY = 550
bgroadX_change = 50

def road(x,y):
    screen.blit(bgroad,(x,y))


#bird wings up
birdupimg = pygame.image.load("FP_BIRD_Birdup.png")
birdupimg = pygame.transform.scale(birdupimg, (50,50))

#bird wings down
birddownimg = pygame.image.load("FP_BIRD_Birddown.png")
birddownimg = pygame.transform.scale(birddownimg, (50,50))

#bird flying
birdX = 200
birdY = 200
birdY_change = 40

def bird(x,y):
    screen.blit(birddownimg, (x,y))
    pygame.display.update()
    t.sleep(0.5)
    screen.blit(birdupimg, (x,y))
    pygame.display.update()
    t.sleep(0.5)
    pygame.display.update()


#pipe
screen_ylength = 600
pipe_gap = 200
base_dist = 50
pipeup_height=[]
pipedown_height = []
pipe_X = []
pipe_Xchange = []
pipedown_img=[]
pipeup_img=[]
y1 = []
no_pipes=5
for i in range (no_pipes):
    pipeup_height.append(random.randrange(100,300))
    pipedown_height.append(screen_ylength-(pipeup_height[i] + pipe_gap + base_dist))
    pipedown_image = pygame.image.load("kindpng_2032468.png").convert_alpha()
    pipedown_img.append(pygame.transform.smoothscale(pipedown_image, (60,pipedown_height[i])))
    pipeup_image = pygame.image.load("kindpng_2032468.png").convert_alpha()
    pipeup_image = pygame.transform.rotate(pipeup_image, 180)
    pipeup_img.append(pygame.transform.smoothscale(pipeup_image, (60,pipeup_height[i])))
    pipe_X=[400,650,900,1150,1400]
    pipe_Xchange.append(40)
    y1.append(550 - pipedown_height[i])  # screen_ylength - base_distance = 550, y1 = coordinate of head of downpipe
    def pipedown(x,y,i):
        screen.blit(pipedown_img[i], (x,y))
    def pipeup(x,y,i):
        screen.blit(pipeup_img[i], (x,y))
        

#collision
def ifcollision(birdX,birdY,pipe_X,y1):
    if (birdX+25)>=pipe_X and birdX<(pipe_X+60):
            if (birdY)<=(y1-200) or (birdY+50)>=y1:
                return True

#score board text
score_value= 0
score_font = pygame.font.Font("SP_INV_Font.otf", 35)

touch_count=0

textX = 10
textY = 550

def show_score(x,y):
    score= score_font.render("SCORE : " + str(score_value), True, (255,255,255), (100,0,0))
    screen.blit(score, (x,y))


#game over text
over_font = pygame.font.Font("SP_INV_Font.otf", 80)

def game_over():
    over = over_font.render(" GAME OVER " , True, (255,0,0))
    screen.blit(over, (130,250))    

#game loop
flying = True
while flying:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flying = False

        #keystroke
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                birdY_change = -50
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                birdY_change = 50
                

    #rgb --> red,green,blue
    screen.fill((0,0,0))
    screen.blit(background,(0,0))


    #tree1 recall
    tree1(bgtree1X,bgtree1Y)
    bgtree1X -= bgtree1X_change

    if bgtree1X < -250:
        bgtree1X = -100


    #tree2 recall
    tree2(bgtree2X,bgtree2Y)
    bgtree2X -= bgtree2X_change

    if bgtree2X < 100:
        bgtree2X = 300

    
    #road recall
    road(bgroadX,bgroadY)
    bgroadX -= bgroadX_change

    if bgroadX < -100:
        bgroadX = 0


    #pipe recall
    for i in range(no_pipes):
        pipe_X[i] -= pipe_Xchange[i]
        pipedown(pipe_X[i],y1[i],i)
        pipeup(pipe_X[i],0,i)

        if pipe_X[i] < 0:
            pipe_X [i] = 1180

        if birdX>=(pipe_X[i]+30) and birdX<=(pipe_X[i]+50):
            if birdY>(y1[i]-100) and (birdY+50)<y1[i]:
                score_value+=1


        #collision detect
        collision = ifcollision(birdX,birdY,pipe_X[i],y1[i])
        if collision:
            col_sound = mixer.Sound("SP_INV_Explosion.wav")
            col_sound.play()
            no_pipes=0
            bgtree1Y=1000
            bgtree2Y=1000
            bgroadY=1000
            birdY = 700
            break
            

    #score board recall
    show_score(textX,textY)
    if collision:
        game_over()
    
    #bird recall
    birdY += birdY_change
    bird(birdX,birdY)


    pygame.display.update()
    fpsclock.tick(FPS)
