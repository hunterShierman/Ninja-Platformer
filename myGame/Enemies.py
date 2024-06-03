import pygame
from random import randint

class Enemy():


    def __init__(self, pos, width, dim, damage, health):

        self.damage = damage

        self.colour = (255, 0, 0)
        
        self.timer = 0
        self.coolDown = 30
        self.onCool = False
        self.drawWeapon = False


        self.width = dim[0]
        self.height = dim[1]
        # width is the width of the platform its on
        self.pos = [randint(pos[0], pos[0] + width - self.width), pos[1] - self.height]
        self.health = health

    def updatePosition(self, screenSpeed):  
        self.pos[0] -= screenSpeed

        # cooldown
        if self.timer < self.coolDown - 7:
            self.drawWeapon = False
        if self.onCool == True:
            self.timer -= 1
            if self.timer <= 0:
                self.onCool = False
    
    def collideBox(self):
        box = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        return box

    def takeDamage(self, dam):
        self.colour = (100, 0, 0)
        self.health -= dam
        return self.health
    
    def primaryAttack(self):

        sword = pygame.Rect(self.pos[0] - 50, self.pos[1] - 50, 150, 100)

        self.coolDown = randint(120, 300)
        self.timer = self.coolDown
        self.onCool = True
        self.drawWeapon = True

        return sword

            
              
         
         





