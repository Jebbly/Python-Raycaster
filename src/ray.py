import math

class Ray:
    def __init__(self, angle, location):
        # Given angle and starting location of ray
        self.angle = math.radians(angle)
        self.location = location

    def calculate(self):
        # Calculate direction of ray
        # If positive, ray is going forward/up
        # If negative, ray is going backwards/down
        x_direction = math.cos(self.angle)
        y_direction = math.sin(self.angle)

        # Find x-coordinate of first intersection between ray and grid
        if x_direction >= 0:
            first_x = math.floor(self.location[0]) + 1 # If ray is facing forward or vertical, add 1 to reach grid value
        elif x_direction < 0:
            first_x = math.floor(self.location[0]) # If ray is facing backward, grid value is equal to floor

        # Find y-coordinate of first intersection between ray and grid
        if y_direction > 0:
            first_y = math.floor(self.location[1]) - 1 # If ray is facing up, subtract 1 from floor to reach grid value
        elif y_direction <= 0:
            first_y = math.floor(self.location[1]) # If ray is facing down or is horizontal, grid value is equal to floor

        # Find distance to wall
        hit = False
        while !(hit):
            if map[X][Y] > 0:
                hit = True
