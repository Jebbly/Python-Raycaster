# Import PyGame and PyGame constants
import pygame
from pygame.locals import *

# Import Camera class
from camera import Camera

# Initialize PyGame
pygame.init()

# Create new Camera Object and define Resolution/FOV
player = Camera((640, 360), 60)

# Setup clock for FPS
FPS = 20
fpsclock = pygame.time.Clock()

# Create display based off of defined resolution
screen = pygame.display.set_mode(player.resolution)

# Variable to keep loop running
running = True

# Main loop!
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

    # Creates dictionary that stores keys pressed
    # Use pressed keys to update player location and rotation
    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)

    # Casts rays and updates display
    player.cast(screen)

    # After loop, wait a certain amount of time so framerate is consistent
    fpsclock.tick(FPS)
