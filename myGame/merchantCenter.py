import pygame 
from Player import Player 
import os

def merchant_center(list_attributes):


    pygame.init()

    #set frame rate
    clock = pygame.time.Clock()
    FPS = 60


    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))


    #world variables 
    run = True 
    scale = 0.8
    button_scale = 0.5
    GRAVITY = 0.7


    #player variables
    moving_right = False
    moving_left = False 



    #load text
 
    #bottom text
    font = pygame.font.SysFont("impact", 30)
    text4 = font.render(f"30 Gold Per Upgrade", True, (0,0,0))
    text4_rect = text4.get_rect(center=(width*0.74, 55)) # Center the text4


    font2 = pygame.font.SysFont("pixelart", 35)
    text2 = font2.render(f"Welcome To My Shop!", True, (255,255,0))
    text2_rect = text2.get_rect(center=(width//2 +50, 275)) # Center the text

    font3 = pygame.font.SysFont("pixelart", 35)
    text3 = font2.render(f"Use Gold to Upgrade Your Stats!", True, (255,255,0))
    text3_rect = text3.get_rect(center=(width//2 +50, 275)) # Center the text

    #stats
    font4 = pygame.font.SysFont("impact",30)

    text = font4.render(f"Current Gold: {list_attributes[0]}", True, (0,0,0))
    text_rect = text.get_rect(center=(width*0.29, 220)) # Center the text

    health_text= font4.render(f"{list_attributes[1]:.0f}", True, (0,0,0))
    health_text_rect = health_text.get_rect(center=(285, 55 )) # Center the text

    sword_text = font4.render(f"{list_attributes[2]}", True, (0,0,0))
    sword_text_rect = sword_text.get_rect(center=(145, 115)) # Center the swordr_text

    swordr_text = font4.render(f"{list_attributes[3]}", True, (0,0,0))
    swordr_text_rect = swordr_text.get_rect(center=(590, 115)) # Center the text

    magic_text = font4.render(f"{list_attributes[4]}", True, (0,0,0))
    magic_text_rect = magic_text.get_rect(center=(150, 166)) # Center the text

    magicr_text = font4.render(f"{list_attributes[5]}", True, (0,0,0))
    magicr_text_rect = magicr_text.get_rect(center=(590, 166)) # Center the text

    magic_c_text = font4.render(f"{list_attributes[6]}", True, (0,0,0))
    magic_c_text_rect = magic_c_text.get_rect(center=(370, 115)) # Center the text

    blockd_text = font4.render(f"{list_attributes[7]}", True, (0,0,0))
    blockd_text_rect = blockd_text.get_rect(center=(365, 165)) # Center the text

    blockc_text = font4.render(f"{list_attributes[8]}", True, (0,0,0))
    blockc_text_rect = blockc_text.get_rect(center=(590, 217)) # Center the text





    #load images 
    backg = pygame.image.load("myGame/img/forest.png")
    back_grect = backg.get_rect()
    backg = pygame.transform.scale(backg, (640, 480))

    market = pygame.image.load("Mygame/img/shop.png")
    market_rect = market.get_rect()
    market = pygame.transform.scale(market, (int(market.get_width() * 0.6), int(market.get_height() * 0.6)))
    market_rect.midbottom = (width//2 + width//4, 600)

    witch = pygame.image.load("Mygame/img/witch.png")
    witch = pygame.transform.flip(witch, True, False)
    witch_rect = witch.get_rect()
    witch = pygame.transform.scale(witch, (int(witch.get_width() * 0.5), int(witch.get_height() * 0.5)))

    gold_i = pygame.image.load("Mygame/img/icons/gold.png")
    gold_i = pygame.transform.flip(gold_i, True, False)
    gold_rect = gold_i.get_rect()
    gold_i = pygame.transform.scale(gold_i, (int(gold_i.get_width() * 0.18), int(gold_i.get_height() * 0.18)))
    gold_rect.center = (125,313)

    #load timer 
    show_text = True
    text_timer = pygame.time.get_ticks()  # Get the current time in milliseconds
    display_duration = 2000  # Duration in milliseconds (2000ms = 2 seconds)




    class Button():
        def __init__(self, image, clicked, x, y, button_scale):
            self.image = pygame.image.load(f"myGame/img/icons/{image}.png")
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * button_scale), int(self.image.get_height() * button_scale)))
            self.rect = self.image.get_rect()
            self.rect.center = (x,y)
            self.clicked = False 

        def draw(self, surface):
            action = False
            #get mouse position
            pos = pygame.mouse.get_pos()

            #check mouseover and clicked conditions
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True

            if pygame.mouse.get_pressed()[0] == 0:
                #draw button on screen
                surface.blit(self.image, (self.rect.x, self.rect.y))
                self.clicked = False

            return action




    #mini player class 
    class Soldier(pygame.sprite.Sprite):

        def __init__(self, char_type, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.direction = 1
            self.flip = False 
            self.vel_y = 0  
            self.jump = False 
            self.in_air = False 
            self.height = 200
            

            #myGame/img/bad_guy.png
            self.image = pygame.image.load(f"myGame/img/{char_type}.png")
            self.rect = self.image.get_rect()
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))

            #animation stuff 
            self.animation_list = []
            self.action = 0
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()




            animation_type = ["player_idle", "player_run", "witch"]
            #load all images for player 
            for animation in animation_type:
                #reset images
                temp_list = []
                #find number of frames for each animation
                num_images = len(os.listdir(f"myGame/img/old_animations/{animation}"))

                #add each frame to list of actions 
                for frame in range(num_images):
                    img = pygame.image.load(f"myGame/img/old_animations/{animation}/{frame}.png")
                    img = pygame.transform.scale(img, (int(img.get_width() * 2), int(img.get_height() * 2)))
                    temp_list.append(img)

                self.animation_list.append(temp_list)
        
            self.image = self.animation_list[self.action][self.frame_index]    
            self.rect = self.image.get_rect()


        
        def move(self, moving_left, moving_right):
            dx = 0
            dy = 0
  

            #moving left 
            if moving_left is True:
                dx = -5
                self.flip = True 
                self.direction = -1
    

                running = pygame.transform.scale(player.image, (self.height+20, self.height))
                running = pygame.transform.flip(running, True, False)
                screen.blit(running, (player.rect.x, player.rect.y+110))
                player.update_action(1)
                player.update_animation()
            
            #moving right 
            if moving_right is True:
                dx = 5
                self.flip = False 
                self.direction = 1

                running = pygame.transform.scale(player.image, (self.height+20, self.height))
                # running = pygame.transform.flip(running, True, False)
                screen.blit(running, (player.rect.x, player.rect.y+110))
                player.update_action(1)
                player.update_animation()




            #jumping 
            if self.jump is True:
                self.vel_y = -11 
                self.jump = False 
                self.in_air = True

            if self.jump is False and moving_left is False and moving_right is False:

                if self.direction == -1:
                    running = pygame.transform.scale(player.image, (self.height, self.height))
                    running = pygame.transform.flip(running, True, False)
                    screen.blit(running, (player.rect.x, player.rect.y+100))
                    player.update_action(0)
                    player.update_animation()

                if self.direction == 1:
                    running = pygame.transform.scale(player.image, (self.height, self.height))
                    screen.blit(running, (player.rect.x, player.rect.y+100))
                    player.update_action(0)
                    player.update_animation()




             

            #apply gravity 
            self.vel_y += GRAVITY 
            dy += self.vel_y 
            if self.vel_y > 10:
                self.vel_y = 10 

            #check if collision 
            if self.rect.bottom + dy > 470:
                dy = 470 - self.rect.bottom
                self.in_air = False 


            #update new coordinates/movement 
            self.rect.x += dx 
            self.rect.y += dy 


        def draw(self):
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * scale), int(self.image.get_height() * scale)))
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

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



        

    def draw_background(gold):
        screen.blit(backg, back_grect)
        screen.blit(market, (width//2+20, 250))
        # screen.blit(witch, (width//2 -125, 300))
        screen.blit(text4, text4_rect)

        text2_rect[0] -= 2
        screen.blit(text2, text2_rect)

        if text2_rect[0] < -300:
            text3_rect[0] -= 2
            screen.blit(text3, text3_rect)


        #draw witch 
        witch_animation = pygame.transform.scale(merchant.image, (merchant.height*0.7, merchant.height*0.7))
        witch_animation = pygame.transform.flip(witch_animation, True, False)
        screen.blit(witch_animation, (240, 290))
        merchant.update_action(2)
        merchant.update_animation()

            


    def reset_gold(list_attributes):

        text = font.render(f"Current Gold: {list_attributes[0]}", True, (0,0,0))
        screen.blit(text, text_rect)
        screen.blit(gold_i, gold_rect)

        health_text = font.render(f"{list_attributes[1]:.0f}", True, (0,0,0))
        screen.blit(health_text, health_text_rect)
     
        sword_text = font.render(f"{list_attributes[2]}", True, (0,0,0))
        screen.blit(sword_text, sword_text_rect)
  
        swordr_text = font.render(f"{list_attributes[3]}", True, (0,0,0))
        screen.blit(swordr_text, swordr_text_rect)

        magic_text = font.render(f"{list_attributes[4]}", True, (0,0,0))
        screen.blit(magic_text, magic_text_rect)

        magicr_text = font.render(f"{list_attributes[5]}", True, (0,0,0))
        screen.blit(magicr_text, magicr_text_rect)

        magic_c_text = font.render(f"{list_attributes[6]}", True, (0,0,0))
        screen.blit(magic_c_text, magic_c_text_rect)

        blockd_text = font.render(f"{list_attributes[7]}", True, (0,0,0))
        screen.blit(blockd_text, blockd_text_rect)

        blockc_text = font.render(f"{list_attributes[8]}", True, (0,0,0))
        screen.blit(blockc_text, blockc_text_rect)



    #define objects
    player = Soldier("ninja_idle", 100, 500)
    merchant = Soldier("witch", width, 500)
    merchant.image = witch

    #buttons 
    # gold = Button("gold", False, 40, 220, 0.2)
    health = Button("health", False, 150, 50, 0.55)
    sword_d = Button("sword", False, 75, 115, 0.3)
    sword_r = Button("sword_r", False, 495, 115, 0.3)
    magic_d = Button("magic", False, 75, 165, 0.3)
    magic_r = Button("magic_r", False, 495, 165, 0.3)
    magic_c = Button("magic_c", False, 275, 115, 0.3)
    block_d = Button("block_dur", False, 278, 165, 0.3)
    block_c = Button("block_c", False,495, 215, 0.3)




    count = 0 


    while run is True:

        # fill_background()
        clock.tick(FPS)
        draw_background(list_attributes[0])

        # player.draw()
        player.move(moving_left, moving_right)
        
        

        if health.draw(screen) is True and list_attributes[0] >30:
            list_attributes[0] -= 30
            list_attributes[1] += 5 

        if sword_d.draw(screen) is True and list_attributes[0] >30:
            list_attributes[0] -= 30
            list_attributes[2] += 5 

        if sword_r.draw(screen) is True and list_attributes[0] >30:
            list_attributes[0] -= 30
            list_attributes[3] += 5 

        if magic_d.draw(screen) is True and list_attributes[0] > 30:
            list_attributes[0] -= 30
            list_attributes[4] += 5 

        if magic_r.draw(screen) is True and list_attributes[0] > 30:
            list_attributes[0] -= 30
            list_attributes[5] += 5 

        if magic_c.draw(screen) is True and list_attributes[0] >30:
            list_attributes[0] -= 30
            list_attributes[6] -= 5 

        if block_d.draw(screen) is True and list_attributes[0] > 30:
            list_attributes[0] -= 30
            list_attributes[7] += 5 

        if block_c.draw(screen) is True and list_attributes[0] >30:
            list_attributes[0] -= 30
            list_attributes[8] -= 5 

        reset_gold(list_attributes)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 

            #keyboard presses ``
            if event.type == pygame.KEYDOWN:
                #move left 
                if event.key == pygame.K_a:
                    moving_left = True 

                
                #move right
                elif event.key == pygame.K_d:
                    moving_right = True


                #jump
                elif event.key == pygame.K_SPACE: 
                    player.jump = True



                if event.key == pygame.K_ESCAPE:
                    run = False 

            #keyboard button released
            if event.type == pygame.KEYUP:
                #stop moving left 
                if event.key == pygame.K_a:
                    moving_left = False 
      
                #stop moving right
                elif event.key == pygame.K_d:
                    moving_right = False 
     

            if player.rect.x > 550:
                run = False 


      


        #update


        #draw 

        pygame.display.flip()

    return list_attributes 


# stats = [100, 50, 5, 100, 10, 150, 120, 10, 130]
# stats = merchant_center(stats)
# print(stats[1])