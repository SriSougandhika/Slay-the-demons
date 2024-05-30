import pygame
import random
from pygame import mixer
mixer.init()

mixer.music.load("BattleMusic.mp3")
mixer.music.play(-1)

pygame.init()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("DEMON SLAYER")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)
bg = pygame.image.load("bgjp.png")
# SLAYER:
slayer = pygame.image.load("swordsman.png")
slayerX = 370
slayerY = 480
sXC = 0
sYC = 0
def player(x,y):
    screen.blit(slayer,(x,y))

# DEMON:
dl = ["demon.png", "demon2.png", "demon3.png"]
enemy = []
enemyX = []
enemyY = []
eXC = []
eYC = []
numEnemies = 6
for i in range(numEnemies):
    enemy.append(pygame.image.load(random.choice(dl)))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    eXC.append(0.3)
    eYC.append(40)

def demon(x,y):
    global numEnemies
    for i in range(numEnemies):
        screen.blit(enemy[i],(x[i],y[i]))

# SWORD FLOW OR HIT:
bullet = pygame.image.load("fire.png")
bulletX=0
bulletY=480
bXC=0
bYC=0.8
bState= "ready"

def fireBullet(X,Y):
    global bState
    bState = "fire"
    screen.blit(bullet,(X+16,Y+10))

# COLLISION DETECTION & KILLING DEMON:
score = 0


def isColl(eX, eY, bX, bY):
    dist = (((eX-bX)**2)+((eY-bY)**2))**0.5
    if dist < 30:
        return True
    else:
        return False

def distances(eX, eY, bX, bY):
    dist = (((eX-bX)**2)+((eY-bY)**2))**0.5
    if dist < 10:
        return True
    else:
        return False
# TEXT:
font = pygame.font.Font("Corporation Games.otf",30)
tX = 10
tY = 10
def showScore():
    global score
    scoreR = font.render("SCORE : "+str(score), True, (102,0,102))
    screen.blit(scoreR,(tX,tY))

go = pygame.font.Font("Corporation Games.otf",60)
def gameover():
    overtext1 = go.render('--GAME OVER--', True, (102,0,102))
    screen.blit(overtext1, (180,250))
    overtext2 = go.render('--Play Again--', True, (102, 0, 102))
    screen.blit(overtext2, (180, 280))
    overtext3 = go.render('--Quit--', True, (102, 0, 102))
    screen.blit(overtext3, (180, 310))
uw = pygame.font.Font("Corporation Games.otf",60)
def userwins():
    wintext1 = uw.render('--USER WINS!--', True, (102,0,102))
    screen.blit(wintext1, (180,250))
    wintext2 = uw.render('--Play Again--', True, (102, 0, 102))
    screen.blit(wintext2, (180, 280))
    wintext3 = uw.render('--Quit--', True, (102, 0, 102))
    screen.blit(wintext3, (180, 310))

run = True

while run:
    screen.fill((0, 0, 0))
    screen.blit(bg,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                sXC = -0.5
            if event.key == pygame.K_RIGHT:
                sXC = 0.5
            if event.key == pygame.K_SPACE and bState == "ready":
                bsound = mixer.Sound("SwordSlash.mp3")
                bsound.play()
                bulletX = slayerX
                fireBullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                sXC = 0
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)
            if distances(pos[0], pos[1], 180,280):
                continue
            elif distances(pos[0], pos[1], 180, 310):
                run = False
    slayerX += sXC
    if slayerX <= 0:
        slayerX = 0
    elif slayerX >= 730:
        slayerX = 730
    for i in range(numEnemies):
        enemyX[i] += eXC[i]
        if enemyX[i] <= 0:
            eXC[i] = 0.3
            enemyY[i] += eYC[i]
        elif enemyX[i] >= 730:
            eXC[i] = -0.3
            enemyY[i] += eYC[i]

    if bulletY <= 0:
        bState = "ready"
        bulletY = 480
    if bState == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bYC
    for i in range(numEnemies):
        c = isColl(enemyX[i], enemyY[i], bulletX, bulletY)
        if c:
            csound = mixer.Sound("BloodSplash.mp3")
            csound.play()
            bulletY = 480
            bState = "ready"
            score += 1
            print(score)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

    player(slayerX, slayerY)
    demon(enemyX, enemyY)
    showScore()
    for i in range(numEnemies):
        if enemyY[i] > 400 and score < 10:
            gameover()

            for j in range(numEnemies):
                enemyY[j] = 2000
    if score == 10:
        userwins()
        for j in range(numEnemies):
            enemyY[j] = 2000
    pygame.display.update()
