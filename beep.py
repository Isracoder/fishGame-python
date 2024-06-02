
import pygame
import os

from random import seed
from random import randint


seed(1)
pygame.mixer.init()
pygame.init()

pygame.font.init()

Timer = 60
WIDTH, HEIGHT = 1100, 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0, 0, 0)
BLUE = (0, 80, 140)
FPS = 60
fishHit = pygame.USEREVENT + 1
fishPowered = pygame.USEREVENT + 2
superFishHit = pygame.USEREVENT + 3
txcFishHit = pygame.USEREVENT + 4
DMG = 5
background_sound = pygame.mixer.Sound(
    os.path.join("assets1", "oceanWavesMusic.wav"))
background_sound.play(-1)
numNumSound = pygame.mixer.Sound(os.path.join('assets1', 'numNum.wav'))
owSound = pygame.mixer.Sound(os.path.join('assets1', 'shortOw.wav'))
chompSound = pygame.mixer.Sound(os.path.join('assets1', 'chomp.wav'))
uhOhSound = pygame.mixer.Sound(os.path.join('assets1', 'uhOh.wav'))
yummySound = pygame.mixer.Sound(os.path.join('assets1', 'yummy.wav'))
yaySound = pygame.mixer.Sound(os.path.join('assets1', 'yay1.wav'))

# powerUpSound = pygame.mixer.Sound(os.path.join('assets1', 'numNum.wav'))
# print(pygame.font.get_fonts())


def main():
    # print("\n\nthis is meeee\n")
    trashRects, trashImages = [], []
    addTrash('sock.png', 335, 535, 280, 55, 58, trashRects, trashImages)
    addTrash('brownBoot.png',  335, 700, 320,
             140, 150, trashRects, trashImages)
    addTrash('emptyCup.png', 330, 39, 390, 70, 75, trashRects, trashImages)
    addTrash('wtrBtl.png', 75, 70, 50, 90, 80, trashRects, trashImages)
    addTrash('cigPack.png', 340, 780, 50, 65, 70, trashRects, trashImages)
    addTrash('bag.png', 33, 900, 400, 135, 130, trashRects, trashImages)
    addTrash('sock.png', 330, 538, 297, 70, 75, trashRects, trashImages)
    addTrash('cup.png', 50, 100, 185, 70, 75, trashRects, trashImages)
    addTrash('grayBoot.png', 150, 300, 29, 140, 150, trashRects, trashImages)

    Health, Timer = 50, 60
    currentTime, startTime = 0, 0
    won, lost, first = False, False, True
    running = True
    poweredUp = False
    clock = pygame.time.Clock()
    fishRect.x = 20
    fishShown = fishy
    fishShownRect = fishRect
    txcFish = txcFish1
    txcFishRect1.x = 500
    powerTime, lastTime, lastFish, openTime = 0, 0, 0, 0
    trashHolder = []
    trashImageHolder = []
    removed = []
    lastmove = 0
    points = 0
    while running and not lost and won == False:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN and first:
                startTime = pygame.time.get_ticks()
                first = False
                lastmove = startTime
                lastFish = startTime

            if event.type == fishHit and not poweredUp:
                Health -= DMG
                uhOhSound.play()

            if event.type == fishPowered:
                poweredUp = True
                Health += 5
                superFishRect.x = fishShownRect.x
                superFishRect.y = fishShownRect.y
                fishShown = superFish
                fishShownRect = superFishRect
                yummySound.play()
                powerTime = pygame.time.get_ticks()
                lastTime = powerTime
                # powerUpSound.play()

            if event.type == txcFishHit and not poweredUp:
                Health -= DMG
                moveTxcAway(fishShownRect, txcFishRect1)
                chompSound.play()
                owSound.play()

            if event.type == superFishHit and poweredUp:
                # Health += 2
                points += 1
                numNumSound.play()

            if len(trashRects) < 5:
                print("Less than 5")

        # pygame.display.update
        keysPressed = pygame.key.get_pressed()
        fishMovement(keysPressed, fishShownRect)
        randomizeTrash(trashHolder, trashImageHolder, removed, trashImages)
        manageHits(trashHolder, trashImageHolder)
        txcHit(fishShownRect, txcFishRect1)
        managePower(fishShownRect, powerUpRect, lastTime)
        if not first:
            manageTxcFish(fishShownRect, txcFishRect1)
        tm = pygame.time.get_ticks()

        if tm - lastmove > 300 and first == False:
            moveTrash(lastmove, tm, trashHolder, trashImageHolder)
            # print('Yes')
            lastmove = tm
        if tm // 1000 % 2 == 0 and first == False:
            txcFish = txcFish2

        # if 2000 + openTime < tm and first == False:
        else:
            txcFish = txcFish1

        if fishShownRect.colliderect(powerUpRect) or fishRect.colliderect(powerUpRect):
            superFishRect.x = fishShownRect.x
            superFishRect.y = fishShownRect.y
            fishShown = superFish
            fishShownRect = superFishRect
            powerTime = pygame.time.get_ticks()
            lastTime = powerTime

        currentTime = pygame.time.get_ticks()
        if currentTime - startTime > 60000:
            lost = True

        powerTime = pygame.time.get_ticks()
        if powerTime - lastTime > 1500:  # fish powered for 2 secs
            fishRect.x = fishShownRect.x
            fishRect.y = fishShownRect.y
            fishShown = fishy
            fishShownRect = fishRect
            lastTime = pygame.time.get_ticks()
            poweredUp = False
            powerTime = 0

        if not first:
            Timer = 60 - ((currentTime-startTime) // 1000)

        if Health < 0:
            lost = True

        drawToScreen(txcFish, Health, Timer, points, fishShown,
                     fishShownRect, trashHolder, trashImageHolder, removed)

        if lost == True:
            drawLoss()

        if points >= 170:
            won = True

        if won == True:
            drawWin()

        # if HEAlTH <= 0:
        #     lost = True
    main()


# def setTrash():
#     xLoc = randint(WIDTH-100, WIDTH)
#     yLoc = randint(50, HEIGHT-400)
#     pick = randint(0, len(trashImages)-1)
#     trashRects.append(trashImages[pick])

# fonts


def manageHits(trashHolder, trashImageHolder):
    i = 0
    for rect in trashHolder:

        if rect.colliderect(fishRect):
            pygame.event.post(pygame.event.Event(fishHit))
            trashHolder.remove(rect)
            del trashImageHolder[i]
            break
        elif rect.colliderect(superFishRect):
            pygame.event.post(pygame.event.Event(superFishHit))
            trashHolder.remove(rect)
            del trashImageHolder[i]
        i += 1


def managePower(fishShownRect, powerUpRect, lastTime):
    if fishShownRect.colliderect(powerUpRect):
        pygame.event.post(pygame.event.Event(fishPowered))
    # if lastTime - pygame.time.get_ticks() > 4000:
        powerUpRect.x = randint(0 + 20, WIDTH-150)
        # print(powerUpRect.x)
        powerUpRect.y = randint(0 + 30, HEIGHT - 130)
    # else:
    #     powerUpRect.x = -10

    # if powerUpRect.x < 0:


# trash

trashWidth, trashHeight = 125, 110


def drawToScreen(txcFish, Health, Timer, points,  fishShown, fishShownRect, trashHolder, trashImageHolder, removed):
    drawBackground()
    drawWords(Health, Timer, points)

    WIN.blit(fishShown, (fishShownRect.x, fishShownRect.y))
    WIN.blit(txcFish, (txcFishRect1.x, txcFishRect1.y))
    for i in range(len(trashImageHolder)):
        WIN.blit(trashImageHolder[i], (trashHolder[i].x, trashHolder[i].y))

    WIN.blit(powerUp, (powerUpRect.x, powerUpRect.y))

    pygame.display.update()


def drawBackground():
    WIN.fill(BLUE)
    displaySeaWeed()


# addTrash('selena\'s Piskel.png', 0, 240, 520, 135, 130)
def moveTrash(startTime, time, trashHolder, trashImageHolder):

    for j in range(len(trashHolder)):
        for i in range((time-startTime) // 300):
            if trashHolder[j].x - 15 > 6:
                trashHolder[j].x -= 15
            else:
                trashHolder[j].x = WIDTH - 5


def randomizeTrash(trashHolder, trashImageHolder, removed, trashImages):

    if len(trashImageHolder) < len(trashImages) - 1 and len(trashImages) > 1:

        xLocation = randint(WIDTH-170, WIDTH-50)
        yLocation = randint(20, HEIGHT-200)
        # ang = randint(1, 350)
        # print(len(trashImages))
        pick = randint(0, len(trashImages)-1)
        while pick in removed:
            pick = randint(0, len(trashImages))
        # WIN.blit(trashImages[pick], (xLocation, yLocation))
        # trashImages[pick] = pygame.transform.rotate(trashImages[pick], ang)
        trashImageHolder.append(trashImages[pick])
        trashHolder.append(pygame.Rect(
            xLocation, yLocation, trashWidth, trashHeight))
    # else:
    #     trashImageHolder.pop()
    #     trashHolder.pop()


# fish BAAABA
txcFishWidth, txcFishHeight = 125, 110
txcFish1_image = pygame.image.load(os.path.join('assets1', 'txcFish1.png'))
txcFish1 = pygame.transform.scale(
    txcFish1_image, (txcFishWidth, txcFishHeight))
txcFishRect1 = pygame.Rect(650, 200, txcFishWidth, txcFishHeight)
txcVel = 2
pshBack = 150

txcFish2_image = pygame.image.load(os.path.join('assets1', 'txcFish2.png'))
txcFish2 = pygame.transform.scale(
    txcFish2_image, (txcFishWidth, txcFishHeight))


def manageTxcFish(fishShownRect, txcFishRect1):
    if fishShownRect.x < txcFishRect1.x:
        txcFishRect1.x -= txcVel
    if fishShownRect.y < txcFishRect1.y:
        txcFishRect1.y -= txcVel
    if fishShownRect.x > txcFishRect1.x:
        txcFishRect1.x += txcVel
    if fishShownRect.y > txcFishRect1.y:
        txcFishRect1.y += txcVel


def txcHit(fishShownRect, txcFishRect1):
    if fishShownRect.colliderect(txcFishRect1):
        pygame.event.post(pygame.event.Event(txcFishHit))


def moveTxcAway(fishShownRect, txcFishRect1):
    if fishShownRect.x < txcFishRect1.x:
        txcFishRect1.x += pshBack
    if fishShownRect.y < txcFishRect1.y:
        txcFishRect1.y += pshBack
    if fishShownRect.x > txcFishRect1.x:
        txcFishRect1.x -= pshBack
    if fishShownRect.y > txcFishRect1.y:
        txcFishRect1.y -= pshBack

# def changeFishy(fishShown, fishShownRect):
#     if fishRect.colliderect(powerUpRect):
#         superFishRect.x = fishRect.x
#         superFishRect.y = fishRect.y
#         fishShown = superFish
#         fishShownRect = superFishRect
#         drawToScreen(txcFish1 , Heal)

# def displayTrash():
#     for i in range(len(trashRects)):
#         WIN.blit(trashImages[i], (trashRects[i].x, trashRects[i].y))


fishVel = 7
fishWidth, fishHeight = 100, 80
fishy_image = pygame.image.load(os.path.join('assets1', 'fishy.png'))
fishy = pygame.transform.rotate(
    pygame.transform.scale(fishy_image, (fishWidth, fishHeight)), 0)
fishRect = pygame.Rect(400, 300, fishWidth, fishHeight)

superFish_image = pygame.image.load(os.path.join('assets1', 'superFish.png'))
superFish = pygame.transform.rotate(
    pygame.transform.scale(superFish_image, (fishWidth + 15, fishHeight + 15)), 0)
superFishRect = pygame.Rect(400, 300, fishWidth + 15, fishHeight + 15)


# power up
powerUpWidth, powerUpHeight = 80, 80
powerUp_image = pygame.image.load(os.path.join('assets1', 'powerUp.png'))
powerUp = pygame.transform.rotate(
    pygame.transform.scale(powerUp_image, (powerUpWidth, powerUpHeight)), 340)
powerUpRect = pygame.Rect(129, 350, powerUpWidth, powerUpHeight)


def drawWords(Health, Timer, Points):
    timerFont = pygame.font.SysFont('cabinsketch', 30, 0, 0)
    timerText = timerFont.render(
        "Time remaining : " + str(Timer), 1, (80, 250, 60))

    healthFont = pygame.font.SysFont('cabinsketch', 30, 0, 0)
    HealthText = healthFont.render(
        "Health remaining : " + str(Health), 1, (80, 250, 60))
    PointsFont = pygame.font.SysFont('cabinsketch', 32, 0, 0)
    PointsText = PointsFont.render(
        "Points Gained : " + str(Points), 1, (80, 250, 60))
    WIN.blit(timerText, (5, 5))
    WIN.blit(HealthText, (WIDTH - HealthText.get_width()-5, 5))
    WIN.blit(PointsText, (WIDTH // 2 - PointsText.get_width() // 2, 5))


def addTrash(picName,  angle, xCord, yCord, trashW, trashH, trashRects, trashImages):
    trashName_image = pygame.image.load(os.path.join('assets1', picName))
    trashName = pygame.transform.rotate(pygame.transform.scale(
        trashName_image, (trashW, trashH)), angle)
    trashNameRect = pygame.Rect(xCord, yCord, trashW, trashH)
    trashRects.append(trashNameRect)
    trashImages.append(trashName)


# seaweed image settings
seaweedWidth, seaweedHeight = 220, 330
seaweed_image = pygame.image.load(os.path.join('assets1', 'seaweed1.png'))
seaweed = pygame.transform.rotate(
    pygame.transform.scale(seaweed_image, (seaweedWidth, seaweedHeight)), 0)
seaweedRect = pygame.Rect(400, 400, seaweedWidth, seaweedHeight)
# coral
coralWidth, coralHeight = 90, 80
coral_image = pygame.image.load(os.path.join('assets1', 'weirdcoral.png'))
coral = pygame.transform.rotate(
    pygame.transform.scale(coral_image, (coralWidth, coralHeight)), 0)
coralRect = pygame.Rect(400, 400, coralWidth, coralHeight)


def fishMovement(keysPressed, fishRect):  # prob done
    if (keysPressed[pygame.K_d] or keysPressed[pygame.K_RIGHT]) and fishRect.x + fishVel + fishWidth < WIDTH:
        fishRect.x += fishVel
    if (keysPressed[pygame.K_a] or keysPressed[pygame.K_LEFT]) and fishRect.x - fishVel > 0:
        fishRect.x -= fishVel
    if (keysPressed[pygame.K_w] or keysPressed[pygame.K_UP]) and fishRect.y - fishVel > 0:
        fishRect.y -= fishVel
    if (keysPressed[pygame.K_s] or keysPressed[pygame.K_DOWN]) and fishRect.y + fishVel + fishHeight < HEIGHT:
        fishRect.y += fishVel
    # if fishRect.x + fishWidth + 10 >= txcFishRect1.x and fishRect.x + fishWidth + 10 <= txcFishRect1.x + txcFishWidth and fishRect.y + fishHeight + 10 >= txcFishRect1.y and fishRect.y - 10 <= txcFishRect1.y + txcFishHeight:
    #     drawToScreen(txcFish2)


def displaySeaWeed():  # prob done
    WIN.blit(seaweed, (0, 320))
    WIN.blit(seaweed, (217, 320))
    WIN.blit(seaweed, (450, 320))
    WIN.blit(seaweed, (680, 320))
    WIN.blit(seaweed, (890, 320))
    WIN.blit(coral, (79, 580))
    WIN.blit(coral, (523, 580))
    WIN.blit(coral, (288, 580))
    WIN.blit(coral, (750, 580))


def drawLoss():
    WIN.fill((0, 102, 110))
    lossFont = pygame.font.SysFont('cabinsketch', 30, 0, 0)
    lossText = lossFont.render(
        "YOU LOST , BETTER LUCK NEXT TIME :(", 1, (80, 250, 60))
    WIN.blit(lossText, ((WIDTH // 2) - (lossText.get_width() // 2), HEIGHT // 2))
    pygame.display.update()
    # yaySound.set_volume(1.0)
    yaySound.play()
    pygame.time.delay(2500)


def drawWin():
    WIN.fill((0, 102, 110))
    winFont = pygame.font.SysFont('cabinsketch', 30, 0, 0)
    winText = winFont.render("CONGRATS , YOU WON !!!", 1, (80, 250, 60))
    WIN.blit(winText, ((WIDTH // 2) - (winText.get_width() // 2), HEIGHT // 2))
    pygame.display.update()
    # pygame.mixer.pause()
    yaySound.play()
    pygame.time.delay(2500)
    # yaySound.play()
    # pygame.mixer.unpause()


if __name__ == "__main__":
    main()
