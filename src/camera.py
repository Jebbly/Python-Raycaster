# Import PyGame and PyGame constants
import pygame
from pygame.locals import *

# Import math library for trigonometric functions
import math

# Import pillow to handle texture slices
from PIL import Image, ImageEnhance

# Import Map layout
from map import Map

Map = Map()

# Import Ray class
from ray import Ray

class Camera:
    def __init__(self, resolution, fov):
        # Define starting location and rotation
        self.location = (2,2)
        self.rotation = 315

        # Define movement and rotation speed
        self.movement_speed = 0.1
        self.rotation_speed = 1

        # Get dimensions and FOV
        self.fov = fov
        self.resolution = resolution

        # Calculate distance from camera to projection plane based off of dimensions and FOV
        self.projection_plane_distance = (self.resolution[0]/2)/math.tan(math.radians(self.fov)/2)/16
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

    def calculate_slice(self, intersection, slice_height):
        # Determine which index of the slice should be used
        index = math.floor(intersection * 32)

        # Take column index in texture
        pixel_column = Map.split_wall_texture[index]

        # Find scalar needed to fit the pixel column into slice height
        scalar = (slice_height / pixel_column.height)
        resized_width, resized_height = math.ceil(scalar), math.ceil(pixel_column.height * scalar)

        # Scale slice by scalar and take the first column
        resized_column = pixel_column.resize((resized_width, resized_height)).crop((0, 0, 1, resized_height - 1))

        # Find object intensity relative to slice height and the height of the texture
        if (slice_height > pixel_column.height):
            intensity = 1 - (pixel_column.height / slice_height)
        else:
            intensity = 0

        # Calculate new column after adjusting to intensity
        adjusted_column = ImageEnhance.Brightness(resized_column).enhance(intensity)

        # Convert the column to a surface
        surface = pygame.image.frombuffer(adjusted_column.tobytes(), adjusted_column.size, adjusted_column.mode)

        # Return slice surface
        return surface

    def cast(self, screen):
        screen.fill((0,0,0))
        # Iterate through each column of pixels
        for column in range(self.resolution[0]):
            # Find the ray angle based on rotation and the angle between subsequent rays
            # Angle between subsequent rays is equal to FOV / # of columns
            angle = self.rotation + self.fov/2 - column * self.fov/self.resolution[0]

            # Instantiate Ray and calculate distance to wall
            ray = Ray(angle, self.location)
            (ray_distance, ray_intersection) = ray.calculate_intersection()

            # Adjust distance to account for fishbowl effect
            correct_distance = ray_distance * math.cos(math.radians(angle-self.rotation))

            # Calculate projected wall height relative to distance and projection plane distance/resolution
            projected_wall_height = (self.projection_scalar / correct_distance)

            # Determine shading/texture of wall based on distance and intersection
            slice = self.calculate_slice(ray_intersection % 1, projected_wall_height)

            # Find where the column should be placed
            start_pos = (self.resolution[1] - projected_wall_height)/2

            # Blit the column at the calculated location
            screen.blit(slice, (column, start_pos))

        # Update display after looping through every column of pixels
        pygame.display.flip()
