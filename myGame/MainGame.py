import sys

import pygame
from pygame.locals import *
from Player import Player 
from Platform import Platform
from Enemies import Enemy
from random import randint
from mygame import hunters_chest_upgrades
from merchantCenter import merchant_center 
import os 


pygame.init()

fps = 60
fpsClock = pygame.time.Clock()

width, height = 640, 480
screen = pygame.display.set_mode((width, height))

pygame.font.init()
my_font = pygame.font.SysFont('impact', 30)
my_font2 = pygame.font.SysFont("impact", 25)

#variables
first_time = True 
realGround = height - 100
global ground
ground = height - 100
screenSpeed = 10


platformList = [Platform([0, realGround], [width, 10])]
enemyList = []


#set up timer 
call_interval = 45000  # Interval in milliseconds (60000ms = 1 minute)
call_interval2 = 60000
last_call_time = pygame.time.get_ticks()  # Initialize the last call time
last_call_time2 = pygame.time.get_ticks()

# TIMER_INTERVAL = 50  # Timer interval in milliseconds (1000 ms = 1 second)
# last_action_time = pygame.time.get_ticks()


#init class
player = Player([width, height], ground)

#stats = [100, 50, 5, 100, 10, 150, 120, 10, 130]

# Game loop.

def update():
    global call_interval 
    global call_interval2
    global last_call_time 
    global last_call_time2


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    fpsClock.tick(fps)


    # the speed at which the camera moves
    if player.pos[0] >= width - 200:
        screenSpeed = player.speed
    else:
        screenSpeed = 2

    # updating
    player.updatePosition(screenSpeed, ground)

    for i in platformList:
        boole = i.updatePosition(screenSpeed, width)
        if boole == True:
            spawnEnemy(i.pos, i.width)
    for i in enemyList:
        i.updatePosition(screenSpeed)

    keepGoing = checkBorderPosition()
    attackUpdate()
    if keepGoing == True:
        keepGoing = checkPlayerHealth()
    checkHealth()
    enemyAttack()
    collisionWithGround()
    addRemObjects()


    current_time = pygame.time.get_ticks()
    if current_time - last_call_time >= call_interval:
        merch_center()
        rand = randint(0,1)
        if rand == 0:
            stats = hunters_chest_upgrades(player.getStats())
            player.updateStats(stats)

        last_call_time = current_time 

    # if current_time - last_call_time2 >= call_interval2:
    #     stats = hunters_chest_upgrades(player.getStats())
    #     player.updateStats(stats)
    #     last_call_time2 = current_time  # Reset the last call time

    return keepGoing

def checkBorderPosition():
    if player.pos[0] <= -100:
        keepGoing = False
    elif player.pos[1] >= height:
        keepGoing = False
    else:
        keepGoing = True

    return keepGoing

def checkPlayerHealth():
    keepGoing = True
    if player.health <= 0:
        keepGoing = False
        player.health = player.baseHealth
    return keepGoing


def checkHealth():
    dead = None
    for i in enemyList:
        if i.health <= 0:
            dead = i
        if i.pos[0] <= 0 - i.width:
            dead = i
            break
    if dead is not None:
        enemyList.remove(dead)

def enemyAttack():
    for i in enemyList:
        if i.onCool == False:
            if i.collideBox().colliderect(player.playerRadius()):
                i.colour = (255,70,0)
                if i.primaryAttack().colliderect(player.collideBox()):
                    player.damagePlayer(i.damage)




def playerCombatCollidePrimary():
    if player.primaryOnCool == False:

        for i in enemyList:
            if player.primaryAttack().colliderect(i.collideBox()):
                i.health = i.takeDamage(player.swordDamage)
                if i.health <= 0:
                    player.kills += 1
                    player.gold += 10  + 2 * player.kills

def playerCombatCollideSecondary():
    if player.secondaryOnCool == False:
        for i in enemyList:
            if player.secondaryAttack().colliderect(i.collideBox()):
                i.health = i.takeDamage(player.magicDamage)
                if i.health <= 0:
                    player.kills += 1
                    player.gold += 10 + 2 * player.kills
                    rand = randint(1, 10)
                    # if rand == 1:
                    #     stats = hunters_chest_upgrades(player.getStats())
                    #     player.updateStats(stats)


def spawnEnemy(pos, width):
    placeEnemy = randint(1, 2)
    if placeEnemy == 1:
        enemyList.append(Enemy(pos, width, [50, 50], 10 + 0.2 * player.kills, 10 + 0.2 * player.kills))



def attackUpdate():

    keys = pygame.key.get_pressed()
    mouse = pygame.mouse.get_pressed(num_buttons=3)
    
    if keys[pygame.K_h] or player.drawWeapon == True or mouse == (True, False, False):


        playerCombatCollidePrimary()

    if keys[pygame.K_j] or player.drawSecondary == True or mouse == (False, True, False):
        playerCombatCollideSecondary()

    if keys[pygame.K_LSHIFT]:
        player.update_action(2)
        player.update_animation()
        player.block()


def collisionWithGround():
    global ground

    isColliding = False
    for i in platformList:
        if player.footCollisionBox().colliderect(i.collsionBox()):
            ground = i.pos[1]
            isColliding = True

    if isColliding == False:
        ground = height + 100
#adds platforms and enemies
def addRemObjects():
    if len(platformList) <= 8:

        placePlatForm = randint(1,5)

        if placePlatForm == 1:
            pos = [randint(width, width + 150), randint(120, height-50)]
            dim = [randint(250, 600), 10]
            platformList.append(Platform(pos, dim))

    # removes platforms if they go off the edge of the screen or are too close together
    i = 0
    while i in range(0, len(platformList)):

        if platformList[i].pos[0] <= 0 - 2 * platformList[i].width:
            platformList.pop(i)

        j = i + 1
        while j in range(i + 1, len(platformList)):
            if platformList[i].spawningCollsionBox().colliderect(platformList[j].spawningCollsionBox()):
                platformList.pop(j)
            j += 1

        i += 1

#draws everything to the screen 
def draw(plat, ene, fire, lazer1, lazer2, bckgrnd, running, standing, attack, parry):
    screen.fill((0, 0, 255))
    bckgrnd = pygame.transform.scale(bckgrnd, (width*1.4, height))
    screen.blit(bckgrnd, (0, 0))
    # print(player.health)
    healthCount = my_font.render(f"{player.health:.0f}", False, (0, 0, 0))
    healthImage = pygame.image.load(f"Hackathon/myGame/img/icons/health.png")
    healthImage = pygame.transform.scale(healthImage, (int(healthImage.get_width() * 0.4), int(healthImage.get_height() * 0.4)))

    goldCount = my_font.render(f"{player.gold:.0f}", False, (0,0,0))
    goldImage = pygame.image.load("Hackathon/Mygame/img/icons/gold.png")
    goldImage = pygame.transform.scale(goldImage, (int(goldImage.get_width() * 0.15), int(goldImage.get_height() * 0.15)))

    # swordcCountImage = pygame.image.load("Hackathon/Mygame/img/icons/sword_c.png")
    # swordcCountImage = pygame.transform.scale(swordcCountImage, (int(swordcCountImage.get_width() * 0.3), int(swordcCountImage.get_height() * 0.3)))

    
    coolDownTimers = my_font2.render(f"{'PrimaryCD':>25}: {player.priaryTimer:<15.0f} SecondaryCD: {player.secondaryTimer:<15.0f} BlockCD: {player.blockingTimer:<10.0f}", False, (0,0,0))
    # print(player.health)
    # pygame.draw.rect(screen, (0,0,0), player.playerRadius())
    # pygame.draw.rect(screen, (0,0,0), player.collideBox())


    for i in platformList:
        plat = pygame.transform.scale(plat, (i.width + 50, i.height + 50))
        # pygame.draw.rect(screen, (0, 255,0), (i.pos[0], i.pos[1], i.width, i.height))
        screen.blit(plat, (i.pos[0] - 20, i.pos[1] - 20))

    for i in enemyList:
        ene = pygame.transform.scale(ene, (i.width +175, i.height +175))
        if player.pos[0] < i.pos[0]:
            ene = pygame.transform.flip(ene, True, False)
        else:
            ene = pygame.transform.flip(ene, False, False)
        # pygame.draw.rect(screen, i.colour, (i.pos[0], i.pos[1], i.width, i.height))

        if i.drawWeapon == True:
            fire = pygame.transform.scale(fire, (i.width+175, i.height+175))
            if player.pos[0] < i.pos[0]:
                fire = pygame.transform.flip(fire, True, False)
                # pygame.draw.rect(screen, (0,0,0), (i.pos[0] - 25, i.pos[1] -  25, 100, 75))
                screen.blit(fire, (i.pos[0]-90, i.pos[1]-113))
            else:
                screen.blit(fire, (i.pos[0]-90, i.pos[1]-113))
        else:
            screen.blit(ene, (i.pos[0] - 90, i.pos[1]-113))

    if player.blocking == False:
        #player
        # pygame.draw.rect(screen, (255, 255, 255), (player.pos[0], player.pos[1], 50, 50))
        if player.isMoving == True:
            if player.facing == 0:
                running = pygame.transform.scale(player.image, (player.pHeight + 150, player.pHeight + 140))
        

                screen.blit(running, (player.pos[0]-25, player.pos[1]-100))
                player.update_action(1)
                player.update_animation()


                
            if player.facing == 1:
                running = pygame.transform.scale(player.image, (player.pHeight + 150, player.pHeight + 140))
                running = pygame.transform.flip(running, True, False)

                screen.blit(running, (player.pos[0]-25, player.pos[1]-100))
                player.update_action(1)
                player.update_animation()


        else:

            if player.facing == 0:
                standing = pygame.transform.scale(player.image, (player.pHeight + 130, player.pHeight + 130))
                screen.blit(standing, (player.pos[0]-25, player.pos[1]-100))
                player.update_action(0)
                player.update_animation()

 
            if player.facing == 1:
                standing = pygame.transform.scale(player.image, (player.pHeight + 130, player.pHeight + 130))
                standing = pygame.transform.flip(standing, True, False)
                screen.blit(standing, (player.pos[0]-25, player.pos[1]-100))
                player.update_action(0)
                player.update_animation()


        # hitbox = player.collideBox()
        # pygame.draw.rect(screen, (0,0,0), hitbox)


        if player.drawWeapon == True:
            if player.facing == 0:

                slash = pygame.transform.scale(attack, (player.pHeight + 130, player.pHeight + 130))
                player.update_action(8)
                player.update_animation()
                screen.blit(slash, (player.pos[0], player.pos[1] - 105))
                # pygame.draw.rect(screen, (0, 0,0), (player.pos[0] - player.pHeight, player.pos[1] - player.pHeight, 100, 100))
                # player.update_action(3)
                # player.update_animation()

            
      

                # pygame.draw.rect(screen, (0,0,0), (player.pos[0], player.pos[1] - player.pHeight, 100, 100))
            if player.facing == 1:
                slash = pygame.transform.scale(attack, (player.pHeight + 130, player.pHeight + 130))
                slash = pygame.transform.flip(slash, True, False)
                player.update_action(8)
                player.update_animation()
                screen.blit(slash, (player.pos[0] - 35, player.pos[1] - 105))
                # pygame.draw.rect(screen, (0, 0,0), (player.pos[0] - player.pHeight, player.pos[1] - player.pHeight, 100, 100))
                # player.update_action(3)
                # player.update_animation()



        if player.drawSecondary == True:
            if player.facing == 0:
                
                lazer1 = pygame.transform.scale(lazer1, (player.magicRange, 50))
                # pygame.draw.rect(screen, (0,0,0), (player.pos[0], player.pos[1], player.magicRange, 50))
                screen.blit(lazer1, (player.pos[0] + 70, player.pos[1]-30))
            else:
                
                lazer2 = pygame.transform.scale(lazer2, (player.magicRange, 50))
                lazer2 = pygame.transform.flip(lazer2, True, False)
                # pygame.draw.rect(screen, (0,0,0), (player.pos[0], player.pos[1], -1 * player.magicRange, 50))
                screen.blit(lazer2, (player.pos[0] - 60, player.pos[1]-30))
    else:
        if player.facing == 0:
            parry = pygame.transform.scale(parry, (player.pHeight + 105, player.pHeight + 105))
            screen.blit(parry, (player.pos[0], player.pos[1]-95))
     


        if player.facing == 1:
            parry = pygame.transform.scale(parry, (player.pHeight + 105, player.pHeight + 105))
            parry = pygame.transform.flip(parry, True, False)
            screen.blit(parry, (player.pos[0], player.pos[1]-95))




    screen.blit(healthCount, (205,7))
    screen.blit(healthImage, (20,0))
    screen.blit(goldCount, (435,8))
    screen.blit(goldImage, (400,10))
    # screen.blit(swordcCountImage, (15,400))


    screen.blit(coolDownTimers, (10, height - 30))




    global first_time 

def merch_center():

    stats = merchant_center(player.getStats())

    player.gold = stats[0]
    player.health = stats[1]
    player.swordDamage = stats[2]
    player.swordRange = stats[3]
    player.magicDamage = stats[4]
    player.magicRange = stats[5]
    player.secondaryCoolDown = stats[6]
    player.blockingDuration = stats[7]
    player.blockingCoolDown = stats[8]


# if first_time is True:
#     merch_center()
#     first_time = False 
# else:
#     rand = randint(1,1000)
#     if rand == 5:
#         merch_center()




keepGoing = True


plat = pygame.image.load("Hackathon\myGame\img\platform.png")
# plat = pygame.transform.scale(plat, (plat.get_width*0.5(), plat.get_height()*0.5))


ene = pygame.image.load("Hackathon\myGame\img/goblin_idle.png")
fire = pygame.image.load("Hackathon\myGame\img/goblin_attack.png")
lazer1 = pygame.image.load("Hackathon\myGame\img\lazer.png")
lazer2 = pygame.image.load("Hackathon\myGame\img\lazer.png")
bckgrnd = pygame.image.load("Hackathon\myGame\img/backg.png")
running = pygame.image.load("Hackathon\myGame\img/ninja_running.png")
standing = pygame.image.load("Hackathon\myGame\img/ninja_idle.png")
attack = pygame.image.load("Hackathon\myGame\img/ninja_attack.png")
parry = pygame.image.load("Hackathon\myGame\img/ninja_parry.png")
# parry = pygame.image.load("Hackathon\myGame\img/old_animations/player_attack2/4.png")






#create animations 




merch_center()


while keepGoing:

    # if first_time is True:
    #     print("stats before", player.getStats())
    #     print(player.health)
    #     stats = merchant_center(player.getStats())
    #     player.updateStats(stats)
    #     first_time = False 
    #     print("stats after",player.getStats())
    #     print(player.health)



    keepGoing = update()
    draw(plat, ene, fire, lazer1, lazer2, bckgrnd, running, standing, attack, parry)

