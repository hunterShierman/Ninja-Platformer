import pygame
import os 

class Player():

    def __init__(self, screenDim, ground):
        # player stats
        self.gold = 0
        self.health = 50
        self.baseHealth = 50
        self.swordDamage = 5
        self.swordRange = 110
        self.magicDamage = 10
        self.magicRange = 100


        self.blocking = False
        self.blockingDuration = 10
        self.blockingCoolDown = 120
        self.blockingOnCool = False
        self.blockingTimer = 0

        self.kills = 0

        self.ground = ground
        self.pHeight = 30 
        self.pos = [500, self.ground - self.pHeight]
        self.speed = 5
        self.screenDim = screenDim 
        self.flip = False 

        #primary
        self.primaryCoolDown = 30
        self.priaryTimer = 0
        self.primaryOnCool = False
        self.drawWeapon = False

        #secondary
        self.secondaryCoolDown = 300
        self.secondaryTimer = 0
        self.secondaryOnCool = False
        self.drawSecondary = False


        # facing 1 - Left 0 - Right
        self.facing = 0
        self.isMoving = False
        
        # jumping
        self.upSpeed = 0
        self.downSpeed = 0.9
        self.startJumpConstant = -20
        self.jumping = False

        self.boughtItems = 0
        self.cost = 100


        #stuff hunter added 
        self.update_time = pygame.time.get_ticks()
        self.animation_list = []
        self.action = 0
        self.frame_index = 0

        #timer stuff 
        self.attack_duration = 500
        self.attack_start_time = 0


        animation_type = ["player_idle", "player_run", "player_attack", "player_attack2", "player_attacked", "player_death", "player_fall", "player_jump", "blank"]
        #load all images for player 
        for animation in animation_type:
            #reset images
            temp_list = []
            #find number of frames for each animation
            num_images = len(os.listdir(f"Hackathon/myGame/img/old_animations/{animation}"))

            #add each frame to list of actions 
            for frame in range(num_images):
                img = pygame.image.load(f"Hackathon/myGame/img/old_animations/{animation}/{frame}.png")
                img = pygame.transform.scale(img, (int(img.get_width() * 2), int(img.get_height() * 2)))
                temp_list.append(img)

            self.animation_list.append(temp_list)
    
        self.image = self.animation_list[self.action][self.frame_index]    
        self.rect = self.image.get_rect()

    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        #update animation
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1 

        #reset animation list 
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0

    def update_action(self, new_action):
        #check if new action is different from previous
        if new_action != self.action:
            self.action = new_action    
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()



    def updatePosition(self, screenSpeed, ground):

        self.ground = ground
        self.pos[0] -= screenSpeed

        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_a]:
            self.pos[0] -= self.speed
            self.facing = 1
            self.isMoving = True
        elif keys[pygame.K_d]:
            self.pos[0] += self.speed
            self.facing = 0
            self.isMoving = True
        else:
            self.isMoving = False 

        if keys[pygame.K_s]:
            if self.jumping == False:
                self.pos[1] += 30
        if keys[pygame.K_SPACE] and self.jumping == False:
            self.jumping = True
            self.upSpeed = self.startJumpConstant
        
    
        #if the player is not touching anything then act as if they had jumped(falling)
        if self.jumping == False and self.pos[1] != self.ground:
            self.jumping = True

        # after the player preses the jump button have "gravity" act on them
        if self.jumping == True:
            if self.upSpeed < 20:
                self.upSpeed += self.downSpeed
            self.pos[1] += self.upSpeed
            if self.pos[1] >= self.ground - self.pHeight and self.upSpeed > 0: 
                self.pos[1] = self.ground - self.pHeight
                self.jumping = False
                self.upSpeed = 0
        
        # self.start_attack()
        # #get cooldown for cooldown attack and drawing weapon
        # current_time = pygame.time.get_ticks()

        # if self.primaryOnCool:
        #     self.priaryTimer -= 1
        #     if self.priaryTimer <= 0:
        #         self.primaryOnCool = False

        # if self.drawWeapon and self.attack_start_time > 0:
        #     if current_time - self.attack_start_time >= self.attack_duration:
        #         self.drawWeapon = False
        #         self.attack_start_time = None







        # cooldowns
        if self.priaryTimer < self.primaryCoolDown - 7:
            self.drawWeapon = False 

        if self.primaryOnCool == True:
            self.priaryTimer -= 1
            if self.priaryTimer <= 0:
                self.primaryOnCool = False 

        if self.secondaryTimer < self.secondaryCoolDown - 7:
            self.drawSecondary = False
        if self.secondaryOnCool == True:
            self.secondaryTimer -= 1
            if self.secondaryTimer <= 0:
                self.secondaryOnCool = False

        if self.blockingOnCool == True:
            if self.blocking == True:
                if self.blockingTimer < self.blockingCoolDown - self.blockingDuration:
                    self.blocking = False
            if self.blockingTimer <= 0:
                self.blockingOnCool = False

            self.blockingTimer -= 1
        



    # collision box ath the players feet
    def footCollisionBox(self):
        foot = pygame.Rect(self.pos[0], self.pos[1] + self.pHeight - 14.9, self.pHeight, 15)
        return foot
    
    def collideBox(self):
        box = pygame.Rect(self.pos[0]+45, self.pos[1]-30, self.pHeight, self.pHeight)
        return box

    def primaryAttack(self):

        if self.facing == 0:
            sword = pygame.Rect(self.pos[0], self.pos[1] - self.pHeight, self.swordRange, self.swordRange)
        else:
            sword = pygame.Rect(self.pos[0] - self.pHeight, self.pos[1] - self.pHeight, self.swordRange, self.swordRange)
        

        self.priaryTimer = self.primaryCoolDown
        self.primaryOnCool = True
        self.drawWeapon = True

        return sword
    
    def secondaryAttack(self):

        if self.facing == 0:
            beam = pygame.Rect(self.pos[0], self.pos[1], self.magicRange, 50)
        else:
            beam = pygame.Rect(self.pos[0], self.pos[1], -1 * self.magicRange, 50)

        self.secondaryTimer = self.secondaryCoolDown
        self.secondaryOnCool = True
        self.drawSecondary = True 
        
        return beam
    
    def playerRadius(self):
        box = pygame.Rect(self.pos[0], self.pos[1] - 50, 100, 60)
        return box
    
    def damagePlayer(self, damage):
        if self.blocking == False:
            self.health -= damage

    def block(self):


        self.blocking = True
        self.blockingOnCool = True
        self.blockingTimer = self.blockingCoolDown

    def getStats(self):
        stats = [self.gold, self.health, self.swordDamage, self.swordRange, self.magicDamage, self.magicRange, self.secondaryCoolDown, self.blockingDuration, self.blockingCoolDown]
        return stats

    def updateStats(self, stats):
        self.gold = stats[0]
        self.baseHealth = stats[1]
        self.swordDamage = stats[2]
        self.swordRange = stats[3]
        self.magicDamage = stats[4]
        self.magicRange = stats[5]
        self.secondaryCoolDown = stats[6]
        self.blockingDuration = stats[7]
        self.blockingCoolDown = stats[8]

