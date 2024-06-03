 

import pygame
from pygame.locals import *
from random import randint
import time 

def hunters_chest_upgrades(list_attributes):
        

    pygame.init()
    
    fps = 60
    fpsClock = pygame.time.Clock()
    
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))

    #world variables 
    bg = (0,100,100)
    scale = 0.6

    #images 
    backg = pygame.image.load("Hackathon\myGame\img\mountain.png")
    backg = pygame.transform.scale(backg, (640, 480))

    #player variables


    #game variables
    frame_index = 0
    update_time = 0
    text_colour = (255,255,255)
    text_colour2 = (255,160,0)
    x = 0

    #render text text 
    font = pygame.font.SysFont('impact', 50)
    font2 = pygame.font.SysFont('impact', 50)
    font3 = pygame.font.SysFont('impact', 25)
    font4 = pygame.font.SysFont('impact', 20)
    font5 = pygame.font.SysFont('impact', 40)




    #new ability
    text = font.render("New Ability Unlocked!", True, text_colour2)
    text_rect = text.get_rect(center=(width+200, 50)) # Center the text

    #bottom text
    text3 = font3.render(f"Enter E to Open Chest", True, (255,255,255))
    text3_rect = text.get_rect(center=(width//2 + 110, 460)) # Center the text

    #exit text 
    text4 = font.render(f"Moving to Next Area", True, (255,200,0))
    text4_rect = text4.get_rect(center=(width+200, 50)) # Center the text



    def print_stats():

        # gold
        stat1 = font4.render(f"Current Gold: {list_attributes[0]:.0f}", True, text_colour)
        stat1_rect = text.get_rect(center=(width//2 -85, height//2 + 50)) # Center the text
        screen.blit(stat1, stat1_rect)


        # health 
        stat2 = font4.render(f"Current Health: {list_attributes[1]:.0f}", True, text_colour)
        stat2_rect = text.get_rect(center=(width//2 - 85, height//2 + 80)) # Center the text
        screen.blit(stat2, stat2_rect)


        # sword damage
        stat3 = font4.render(f"Current Sword Damage: {list_attributes[2]:.0f}", True, text_colour)
        stat3_rect = text.get_rect(center=(width//2 -85, height//2 + 110)) # Center the text
        screen.blit(stat3, stat3_rect)

        # sword range
        stat4 = font4.render(f"Current Sword Range: {list_attributes[3]:.0f}", True, text_colour)
        stat4_rect = text.get_rect(center=(width//2 -85, height//2 + 140)) # Center the text
        screen.blit(stat4, stat4_rect)

        # magic damage
        stat5 = font4.render(f"Current Magic Damage: {list_attributes[4]:.0f}", True, text_colour)
        stat5_rect = text.get_rect(center=(width//2 -85, height//2 + 170)) # Center the text
        screen.blit(stat5, stat5_rect)


        # magic range
        stat6 = font4.render(f"Current Magic Range: {list_attributes[5]:.0f}", True, text_colour)
        stat6_rect = text.get_rect(center=(width -28, height//2 + 50)) # Center the text
        screen.blit(stat6, stat6_rect)

        # magic cooldown
        stat7 = font4.render(f"Current Magic Cooldown {list_attributes[6]:.0f}", True, text_colour)
        stat7_rect = text.get_rect(center=(width-28, height//2 + 80)) # Center the text
        screen.blit(stat7, stat7_rect)

        # block duration
        stat8 = font4.render(f"Current Block Duration: {list_attributes[7]:.0f}", True, text_colour)
        stat8_rect = text.get_rect(center=(width-28, height//2 + 110)) # Center the text
        screen.blit(stat8, stat8_rect)

        # block cooldown
        stat10 = font4.render(f"Current Block Cooldown: {list_attributes[8]:.0f}", True, text_colour)
        stat10_rect = text.get_rect(center=(width-28, height//2 + 140)) # Center the text
        screen.blit(stat10, stat10_rect)


    class chest(pygame.sprite.Sprite):

        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            
            self.update_time = pygame.time.get_ticks()
            self.animation_list = []
            self.frame_index = 0

            #load all images for player 
            #add each frame to list of actions 
            for frame in range(2):
                img = pygame.image.load(f"Hackathon\myGame\img\{frame}.png")
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                self.animation_list.append(img)

            self.animation_list.append(img)

            self.image = self.animation_list[self.frame_index]    
            self.rect = self.image.get_rect()
            self.rect.center = (310,260)



        def new_upgrade(self, list_attributes):

            random_num = randint(0,8)

            #update gold 
            if random_num == 0:
                list_attributes[0] += 500
                text2 = font2.render("Gold Increased!", True, text_colour2)
                text2_rect = text.get_rect(center=(width+200, 50)) # Center the text


            #update health 
            elif random_num == 1:
                list_attributes[1] += 15
                text2 = font2.render("Health Increased!", True, text_colour2)
                text2_rect = text.get_rect(center=(width+200, 50)) # Center the text

            #update sword damage 
            elif random_num == 2:
                list_attributes[2] += 5
                text2 = font2.render("Sword Damage Increased", True, text_colour2)
                text2_rect = text.get_rect(center=(width+200, 50)) # Center the text



            #update sword range
            elif random_num == 3:
                list_attributes[3] += 10
                text2 = font2.render("Sword Damage Increased!", True, text_colour2)
                text2_rect = text.get_rect(center=(width+200, 50)) # Center the text


            #update magic damage 
            elif random_num == 4:
                list_attributes[4] += 10
                text2 = font2.render("Magic Damage Increased!", True, text_colour2)
                text2_rect = text.get_rect(center=(width+200, 50)) # Center the text



            #update magic range 
            elif random_num == 5:
                list_attributes[5] += 30
                text2 = font2.render("Magic Range Increased!", True, text_colour2)
                text2_rect = text.get_rect(center=(width+200, 50)) # Center the text


            #update magic cooldown
            elif random_num == 6:
                list_attributes[6] -= 20
                text2 = font2.render("Magic Cooldown Decreased!", True, text_colour2)
                text2_rect = text.get_rect(center=(width+200, 50)) # Center the text


            #update block duration
            elif random_num == 7:
                list_attributes[7] += 5
                text2 = font2.render("Block Duration Increased!", True, text_colour2)
                text2_rect = text.get_rect(center=(width+200, 50)) # Center the text



            #update block cooldown
            elif random_num == 8:
                list_attributes[8] -= 15
                text2 = font2.render("Block Cooldown Decreased!", True, text_colour2)
                text2_rect = text.get_rect(center=(width+200, 50)) # Center the text


            return text2, text2_rect

        def draw(self):
            screen.blit(backg, (0,0))
            screen.blit(text3, text3_rect)
            screen.blit(self.image, self.rect)


        def update_animation(self):
            ANIMATION_COOLDOWN = 1000
            #update animation

            if self.frame_index <= 2:
                self.image = self.animation_list[self.frame_index]
                if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                    self.update_time = pygame.time.get_ticks()
                    self.frame_index += 1 
                
        


    che = chest()



    run = True
    count = 0
    action_started = False

    while run is True:


        # fill_background()
        che.draw()

        for event in pygame.event.get():
            if event.type == QUIT:
                run = False 
            

            if event.type == KEYDOWN:
                if event.key == K_e and not action_started:
                    action_started = True

                    # Only call once
                    if count == 0:
                        text2, text2_rect = che.new_upgrade(list_attributes)
                        count += 1

        # Continue the series of actions
        if action_started:

            che.update_animation()
            print_stats()

            # Print first letters to screen
            text_rect[0] -= 4
            screen.blit(text, text_rect)

            # Print type of upgrade
            if text2 and text_rect[0] < 0:
                text2_rect[0] -= 4
                screen.blit(text2, text2_rect)

            if text2_rect[0] < -600:
                run = False 



        #update

        #draw 

        pygame.display.flip()
        fpsClock.tick(60)

    # pygame.quit()
    return list_attributes

# gold = 0
# health = 0
# sword_d= 0
# sword_r= 0
# magic_d = 0
# magic_r = 0
# magic_c = 0
# block_dur = 0
# block_c = 0

# list_attributes = [gold, health, sword_d, sword_r, magic_d, magic_r, magic_c, block_dur, block_c]
# hunters_chest_upgrades(list_attributes)


