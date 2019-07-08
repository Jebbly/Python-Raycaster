from PIL import Image

# Open images
BRICK = Image.open("../resources/textures/Brick/Brick-32x32.png")
WOOD = Image.open("../resources/textures/Wood/Wood-32x32.png")

# Define constants
RESOLUTION = (320, 200)
FOV = 60
WALL_TEXTURE = WOOD
FLOOR_TEXTURE = BRICK
