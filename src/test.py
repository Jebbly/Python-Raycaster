import math

from map import Map

class Ray:
    def __init__(self, angle, location):
        # Given angle and starting location of ray
        self.angle = math.radians(angle)
        self.x, self.y = location[0], location[1]

        # Calculate direction of ray
        # If statements will check if the result is supposed to be 0 (math library approximates results)
        if angle % 180 == 90:
            self.x_direction = 0
        else:
            self.x_direction = math.cos(self.angle)

        if angle % 180 == 0:
            self.y_direction = 0
        else:
            self.y_direction = math.sin(self.angle)

    def calculate_distance(self):
        # Find the first horizontal and vertical intersections with walls
        distance_to_horizontal_intersection = self.test_horizontal()
        distance_to_vertical_intersection = self.test_vertical()

        print(distance_to_horizontal_intersection, distance_to_vertical_intersection)

        # Compare the distances and take the lower one (intersects first)
        if (distance_to_horizontal_intersection <= distance_to_vertical_intersection):
            distance = distance_to_horizontal_intersection
        else:
            distance = distance_to_vertical_intersection

        # Return distance from ray to nearest intersection
        print(distance)

    def test_horizontal(self):
        # Find y-coordinate of first intersection between ray and grid (and other values)
        if self.y_direction > 0:
            y_intersection = math.floor(self.y) # If ray is facing up, y-coordinate is equal to floor
            grid_y = y_intersection - 1 # When ray faces up, the intersection belongs to the upper grid
            step_y = -1 # Vertical step of -1 for later increments
        elif self.y_direction < 0:
            y_intersection = math.ceil(self.y) # If ray is facing down, y-coordinate is equal to ceiling
            grid_y = y_intersection # WHen ray faces down, the intersection belongs to the lower grid
            step_y = 1 # Vertical step of 1 for later increments
        else:
            return math.inf # If ray is completely horizontal, there is no intersection

        # Find vertical distance from original location to intersection
        delta_y = self.y - y_intersection

        # Use delta y to find horizontal distance from original location to intersection
        if (self.x_direction == 0): # If ray is vertical then the x value won't change
            delta_x = 0
            step_x = 0
        else: # Otherwise use tangent to calculate distance from original location to first intersection and step x
            delta_x = delta_y / math.tan(self.angle)
            step_x = step_y / math.tan(self.angle)

        #Find x-coordinate of first intersection between ray and grid (and other values)
        x_intersection = self.x + delta_x # Use horizontal distance to find x-coordinate of first intersection
        grid_x = math.floor(x_intersection) # Find grid location of x-coordinate

        # Declare variable to keep track of whether or not ray has hit a wall
        hit = False
        while not hit:
            # Test for map[rounded_y][rounded_x] because of how lists of lists are referenced
            # If the grid has a wall then break out of loop
            if Map[grid_y][grid_x]:
                hit = True
                break

            # Increment current location by step x and step y if wall isn't found
            x_intersection += step_x
            grid_x = math.floor(x_intersection)
            grid_y += step_y

        # Find distance using Pythagorean Theorem
        distance_x = x_intersection - self.x

        # If ray is facing up then the y distance is 1 too great (intersection is considered part of the upper grid)
        if self.y_direction > 0:
            distance_y = grid_y + 1 - self.y
        else:
            distance_y = grid_y - self.y

        distance = math.sqrt(distance_x**2 + distance_y**2)

        # Return the distance to the first horizontal wall intersection
        return distance

    def test_vertical(self):
        # Find x-coordinate of first intersection between ray and grid (and other values)
        if self.x_direction < 0:
            x_intersection = math.floor(self.x) # If ray is facing backwards, x-coordinate is equal to floor
            grid_x = x_intersection - 1 # When ray faces backwards, the intersection belongs to the back grid
            step_x = -1 # Vertical step of -1 for later increments
        elif self.x_direction > 0:
            x_intersection = math.ceil(self.x) # If ray is facing forward, x-coordinate is equal to ceiling
            grid_x = x_intersection # WHen ray faces forward, the intersection belongs to the front grid
            step_x = 1 # Vertical step of 1 for later increments
        else:
            return math.inf # If ray is completely vertical, there is no intersection

        # Find horizontal distance from original location to intersection
        delta_x = self.x - x_intersection

        # Use delta x to find vertical distance from original location to intersection
        if (self.y_direction == 0): # If ray is horizontal then the y value won't change
            delta_y = 0
            step_y = 0
        else: # Otherwise use tangent to calculate distance from original location to first intersection and step y
            delta_y = delta_x * math.tan(self.angle)
            step_y = -step_x * math.tan(self.angle)

        #Find y-coordinate of first intersection between ray and grid (and other values)
        y_intersection = self.y + delta_y # Use vertical distance to find y-coordinate of first intersection
        grid_y = math.floor(y_intersection) # Find grid location of y-coordinate

        # Declare variable to keep track of whether or not ray has hit a wall
        hit = False
        while not hit:
            # Test for map[rounded_y][rounded_x] because of how lists of lists are referenced
            # If the grid has a wall then break out of loop
            if Map[grid_y][grid_x]:
                hit = True
                break

            # Increment current location by step x and step y if wall isn't found
            y_intersection += step_y
            grid_y = math.floor(y_intersection)
            grid_x += step_x

        # Find distance using Pythagorean Theorem
        distance_y = y_intersection - self.y

        # If ray is facing backwards then the x distance is 1 too great (intersection is considered part of the back grid)
        if self.x_direction < 0:
            distance_x = grid_x + 1 - self.x
        else:
            distance_x = grid_x - self.x

        distance = math.sqrt(distance_x**2 + distance_y**2)

        # Return the distance to the first vertical wall intersection
        return distance

ray1 = Ray(60, (96/64, 224/64))
ray2 = Ray(120, (96/64, 224/64))
ray3 = Ray(225, (96/64, 224/64))
ray4 = Ray(180, (96/64, 224/64))
ray1.calculate_distance()
ray2.calculate_distance()
ray3.calculate_distance()
ray4.calculate_distance()
