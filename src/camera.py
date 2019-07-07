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
        self.vertical_rotation = 0

        # Define movement and rotation speed
        self.movement_speed = 0.1
        self.rotation_speed = 3
        self.vertical_rotation_speed = 10

        # Get dimensions and FOV
        self.fov = fov
        self.resolution = resolution

        # Calculate distance from camera to projection plane based off of dimensions and FOV
        self.projection_plane_distance = (self.resolution[0]/2)/math.tan(math.radians(self.fov)/2)/16
        self.projection_scalar = self.projection_plane_distance * Map.wall_height

        # Define height of camera (half of wall height)
        self.height = Map.wall_height / 2

    def update(self, pressed_keys):
        # Set new location and rotation variable
        new_location = list(self.location)
        new_rotation = self.rotation
        new_vertical_rotation = self.vertical_rotation

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

        # Manage vertical rotation
        if pressed_keys[K_UP]:
            new_vertical_rotation += self.vertical_rotation_speed
        if pressed_keys[K_DOWN]:
            new_vertical_rotation -= self.vertical_rotation_speed

        # Detect collisions
        grid_x, grid_y = math.floor(new_location[0]), math.floor(new_location[1])
        if (Map.layout[grid_y][grid_x] == 1):
            new_location[0] = self.location[0]
            new_location[1] = self.location[1]

        # Set vertical rotation boundaries
        if (new_vertical_rotation > self.resolution[1]/3) or (new_vertical_rotation < -self.resolution[1]/3):
            new_vertical_rotation = self.vertical_rotation

        # Return updated location and rotation
        self.location = tuple(new_location)
        self.rotation = new_rotation % 360
        self.vertical_rotation = new_vertical_rotation

    def calculate_color_intensity(self, distance):
        # Calculate intensity relative to distance
        intensity = (1 - (distance / Map.longest_distance))**2

        # Return intensity
        return intensity

    def calculate_slice(self, distance, intersection, slice_height):
        # Determine which index of the slice should be used
        index = math.floor(intersection * len(Map.split_wall_texture))

        # Take column index in texture
        pixel_column = Map.split_wall_texture[index]

        # Find scalar needed to fit the pixel column into slice height
        scalar = (slice_height / pixel_column.height)
        resized_height = math.floor(pixel_column.height * scalar)

        # Scale slice by scalar and take the first column
        resized_column = pixel_column.resize((1, resized_height))

        # Find object intensity
        intensity = self.calculate_color_intensity(distance)

        # Calculate new column after adjusting to intensity
        adjusted_column = ImageEnhance.Brightness(resized_column).enhance(intensity)

        # Convert the column to a surface
        surface = pygame.image.frombuffer(adjusted_column.tobytes(), adjusted_column.size, adjusted_column.mode)

        # Return slice surface
        return surface

    def draw_floor_slice(self, screen, column, pixel_position, ray_angle):
        # Continue to calculate pixels while on screen
        while pixel_position < self.resolution[1]:
            # Use pixel and camera position to find the straight distance from camera to floor intersection
            pixel_distance_to_center = pixel_position - (self.resolution[1] / 2 + self.vertical_rotation)
            straight_distance = self.projection_plane_distance * self.height / pixel_distance_to_center

            # Calculate actual distance
            actual_distance = straight_distance / math.cos(math.radians(ray_angle - self.rotation))

            # Calculate floor intersection
            floor_intersection_x = self.location[0] + (math.cos(math.radians(ray_angle)) * actual_distance)
            floor_intersection_y = self.location[1] - (math.sin(math.radians(ray_angle)) * actual_distance)

            # Find the correct texture index
            texture_x = math.floor((floor_intersection_x % 1) * len(Map.split_floor_texture))
            texture_y = math.floor((floor_intersection_y % 1) * len(Map.split_floor_texture))

            # Find corresponding color
            color = Map.split_floor_texture[texture_x][texture_y]

            # Adjust color according to distance
            intensity = self.calculate_color_intensity(actual_distance)
            adjusted_color = tuple([color_value * intensity for color_value in color])

            # Fill in the pixel
            screen.fill(adjusted_color, (column, pixel_position, 1, 1))

            # Increment to calculate next pixel underneath
            pixel_position += 1

    def cast(self, screen):
        # Fill in background before raycasting
        screen.fill((3, 3, 10))

        # Iterate through each column of pixels
        for column in range(self.resolution[0]):
            # Find the ray angle based on rotation and the angle between subsequent rays
            # Angle between subsequent rays is equal to FOV / # of columns
            angle = self.rotation + self.fov / 2 - column * self.fov / self.resolution[0]

            # Instantiate Ray and calculate distance to wall
            ray = Ray(angle, self.location)
            (ray_distance, ray_intersection) = ray.calculate_intersection()

            # Adjust distance to account for fishbowl effect
            correct_distance = ray_distance * math.cos(math.radians(angle-self.rotation))

            # Calculate projected wall height relative to distance and projection plane distance/resolution
            projected_wall_height = (self.projection_scalar / correct_distance)

            # Determine shading/texture of wall based on distance and intersection
            slice = self.calculate_slice(ray_distance, ray_intersection % 1, projected_wall_height)

            # Find where the column should be placed
            start_pos = (self.resolution[1] - projected_wall_height) / 2 + self.vertical_rotation

            # Blit the column at the calculated location
            screen.blit(slice, (column, start_pos))

            # Fill in the floor pixels underneath
            self.draw_floor_slice(screen, column, start_pos + projected_wall_height - 1, angle)

        # Update display after looping through every column of pixels
        pygame.display.flip()
