import math

import pygame
from pygame.locals import *

class Camera:
    def __init__(self, resolution, fov):
        # Define starting location and rotation
        self.location = (0,0)
        self.rotation = 0

        # Define movement and rotation speed
        self.movement_speed = 0.02
        self.rotation_speed = 0.02

        # Get dimensions and FOV
        self.fov = math.radians(fov)
        self.resolution = resolution

        # Calculate distance from camera to projection plane based off of dimensions and FOV
        self.projection_plane_distance = (self.resolution[0]/2)/math.tan(self.fov/2)

    def update(self, pressed_keys):
        # Convert tuple (immutable) to list (mutable)
        new_location = list(self.location)

        # Manage movement by using sine and cosine to determine direction
        if pressed_keys[K_w]:
            new_location[0] += math.cos(math.radians(self.rotation)) * self.movement_speed
            new_location[1] += math.sin(math.radians(self.rotation)) * self.movement_speed
        if pressed_keys[K_a]:
            new_location[0] -= math.sin(math.radians(self.rotation)) * self.movement_speed
            new_location[1] += math.cos(math.radians(self.rotation)) * self.movement_speed
        if pressed_keys[K_s]:
            new_location[0] -= math.cos(math.radians(self.rotation)) * self.movement_speed
            new_location[1] -= math.sin(math.radians(self.rotation)) * self.movement_speed
        if pressed_keys[K_d]:
            new_location[0] += math.sin(math.radians(self.rotation)) * self.movement_speed
            new_location[1] -= math.cos(math.radians(self.rotation)) * self.movement_speed

        # Manage rotation
        if pressed_keys[K_RIGHT]:
            self.rotation -= self.rotation_speed
        if pressed_keys[K_LEFT]:
            self.rotation += self.rotation_speed

        # Detect collisions

        # Convert list back to tuple and update self.location
        self.location = tuple(new_location)

    def cast(self):

        pygame.display.flip()
