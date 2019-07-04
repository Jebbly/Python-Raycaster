# Import PyGame and PyGame constants
import pygame
from pygame.locals import *

# Import math library for trigonometric functions
import math

# Import Map layout
from map import Map

Map = Map()

# Import Ray class
from ray import Ray

class Camera:
    def __init__(self, resolution, fov):
        # Define starting location and rotation
        self.location = (10,10)
        self.rotation = 315

        # Define movement and rotation speed
        self.movement_speed = 0.1
        self.rotation_speed = 1

        # Get dimensions and FOV
        self.fov = fov
        self.resolution = resolution

        # Calculate distance from camera to projection plane based off of dimensions and FOV
        self.projection_plane_distance = (self.resolution[0]/2)/math.tan(math.radians(self.fov)/2)/32
        self.projection_scalar = self.projection_plane_distance * Map.wall_height

    def update(self, pressed_keys):
        # Set new location and rotation variable
        new_location = list(self.location)
        new_rotation = self.rotation

        # Manage movement by using sine and cosine to determine direction
        if pressed_keys[K_w]:
            new_location[0] += math.cos(math.radians(self.rotation)) * self.movement_speed
            new_location[1] -= math.sin(math.radians(self.rotation)) * self.movement_speed
        if pressed_keys[K_a]:
            new_location[0] -= math.sin(math.radians(self.rotation)) * self.movement_speed
            new_location[1] -= math.cos(math.radians(self.rotation)) * self.movement_speed
        if pressed_keys[K_s]:
            new_location[0] -= math.cos(math.radians(self.rotation)) * self.movement_speed
            new_location[1] += math.sin(math.radians(self.rotation)) * self.movement_speed
        if pressed_keys[K_d]:
            new_location[0] += math.sin(math.radians(self.rotation)) * self.movement_speed
            new_location[1] += math.cos(math.radians(self.rotation)) * self.movement_speed

        # Manage rotation
        if pressed_keys[K_RIGHT]:
            new_rotation -= self.rotation_speed
        if pressed_keys[K_LEFT]:
            new_rotation += self.rotation_speed

        # Detect collisions
        '''grid_x, grid_y = math.floor(new_location[0]), math.floor(new_location[1])

        if (Map.layout[grid_y][grid_x] == 1):
            new_location[0] = self.location[0]
            new_location[1] = self.location[1]'''

        # Return updated location and rotation
        self.location = tuple(new_location)
        self.rotation = new_rotation % 360

    def cast(self, screen):
        screen.fill((0,0,0))
        # Iterate through each column of pixels
        for column in range(self.resolution[0]):
            # Find the ray angle based on rotation and the angle between subsequent rays
            # Angle between subsequent rays is equal to FOV / # of columns
            angle = self.rotation + self.fov/2 - column * self.fov/self.resolution[0]

            # Instantiate Ray and calculate distance to wall
            ray = Ray(angle, self.location)
            ray_distance = ray.calculate_distance()

            # Adjust distance to account for fishbowl effect
            correct_distance = ray_distance * math.cos(math.radians(angle-self.rotation))

            # print("Correct distance: " + str(correct_distance))

            # Calculate projected wall height
            projected_wall_height = (self.projection_scalar / correct_distance)
            # print(projected_wall_height)

            # Draw line equal to column of pixels
            start_pos = (self.resolution[1] - projected_wall_height)/2
            end_pos = start_pos + projected_wall_height
            color = tuple([255/(correct_distance) for x in (100,100,100)])

            pygame.draw.line(screen, color, (column, start_pos), (column, end_pos))

        # Update display after looping through every column of pixels
        pygame.display.flip()
