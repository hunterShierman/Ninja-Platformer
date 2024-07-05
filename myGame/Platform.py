import pygame
from random import randint



class Platform():

    def __init__(self, pos, dim):
        self.pos = pos
        self.width = dim[0]
        self.height = dim[1]
        self.hasEnemy = False

    def updatePosition(self, screenSpeed, width):
        boole = False
        self.pos[0] -= screenSpeed
        if self.pos[0] <= width and self.hasEnemy == False:
            boole = True
            self.hasEnemy = True
        return boole

    def collsionBox(self):
        box = pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
        return box

    def spawningCollsionBox(self):
        padding_x = 50
        padding_y = 50

        box = pygame.Rect(self.pos[0] - padding_x, self.pos[1] - padding_y, self.width + 1.5*padding_x, self.height + 2*padding_y)
        return box