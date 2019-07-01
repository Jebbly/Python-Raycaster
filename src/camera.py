# Import PyGame and PyGame constants
import pygame
from pygame.locals import *

# Import math library for trigonometric functions
import math

# Import Ray class
from ray import Ray

class Camera:
    def __init__(self, resolution, fov):
        # Define starting location and rotation
        self.location = [0,0]
        self.rotation = 0

        # Define movement and rotation speed
        self.movement_speed = 0.02
        self.rotation_speed = 0.02

        # Get dimensions and FOV
        self.fov = fov
        self.resolution = resolution

        # Calculate distance from camera to projection plane based off of dimensions and FOV
        self.projection_plane_distance = (self.resolution[0]/2)/math.tan(math.radians(self.fov)/2)

    def update(self, pressed_keys):
        # Manage movement by using sine and cosine to determine direction
        if pressed_keys[K_w]:
            self.location[0] += math.cos(math.radians(self.rotation)) * self.movement_speed
            self.location[1] += math.sin(math.radians(self.rotation)) * self.movement_speed
        if pressed_keys[K_a]:
            self.location[0] -= math.sin(math.radians(self.rotation)) * self.movement_speed
            self.location[1] += math.cos(math.radians(self.rotation)) * self.movement_speed
        if pressed_keys[K_s]:
            self.location[0] -= math.cos(math.radians(self.rotation)) * self.movement_speed
            self.location[1] -= math.sin(math.radians(self.rotation)) * self.movement_speed
        if pressed_keys[K_d]:
            self.location[0] += math.sin(math.radians(self.rotation)) * self.movement_speed
            self.location[1] -= math.cos(math.radians(self.rotation)) * self.movement_speed

        # Manage rotation
        if pressed_keys[K_RIGHT]:
            self.rotation -= self.rotation_speed
        if pressed_keys[K_LEFT]:
            self.rotation += self.rotation_speed

        # Detect collisions

    def cast(self):
        # Iterate through each column of pixels
        for column in range(self.resolution[0]):
            # Find the ray angle based on rotation and the angle between subsequent rays
            # Angle between subsequent rays is equal to FOV / # of columns
            angle = self.rotation - self.fov/2 + column * self.fov/self.resolution[0]

            # Instantiate Ray and calculate distance to wall
            ray = Ray(angle, self.location)
            ray_distance = ray.calculate_distance()

            # Adjust distance to account for fishbowl effect
            correct_distance = distance * math.cos(math.radians(angle-self.rotation))

        # Update display after looping through every column of pixels
        pygame.display.flip()
