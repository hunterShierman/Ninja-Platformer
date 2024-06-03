import pygame
import sys
from Player import Player 
import time 


# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600
ground = screen_height - 100

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Basic Pygame Game Loop")

# Clock to manage frame rate

clock = pygame.time.Clock()
minute_interval = 1000  # 60 seconds in milliseconds
last_minute_tick = pygame.time.get_ticks()


# Colors

# Player settings
player = Player([screen_width, screen_height], ground)


# Game loop
count = 0

running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle keys
    keys = pygame.key.get_pressed()


    # Update game state
    # (No complex game logic in this basic example)

    # Clear the screen
    screen.fill((0,200,100))
    
    #player stuff 
    screen.blit(player.image, (0,0))
    player.update_animation()

    current_tick = pygame.time.get_ticks()
    if current_tick - last_minute_tick >= minute_interval:
        player.update_action(count)
        count += 1 
        last_minute_tick = current_tick





    # Draw the player

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()