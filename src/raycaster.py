import pygame
from pygame.locals import *

from camera import Camera

pygame.init()

# Create new Camera Object and define Resolution/FOV
player = Camera((320,200), 60)


screen = pygame.display.set_mode(player.resolution)

running = True

while running:
    # for loop through the event queue (all user input + other events go into queue)
    # Queue is accessed through pygame.event.get()
    for event in pygame.event.get():
        # Check for KEYDOWN event
        # KEYDOWN is a constant defined in pygame.locals
        if event.type == KEYDOWN:
            # If the "Esc" key has been pressed, exit main loop by setting running to False
            if event.key == K_ESCAPE:
                running = False
        # Check for QUIT event
        # if QUIT, set running to False
        elif event.type == QUIT:
            running = False

    pressed_keys = pygame.key.get_pressed()

    if pressed_keys:
        player.update(pressed_keys)
        print(player.location, player.rotation)
