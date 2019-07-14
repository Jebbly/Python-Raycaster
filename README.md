# PyCaster: Python Raycaster using PyGame and Pillow
PyCaster is a [raycasting engine](https://en.wikipedia.org/wiki/Ray_casting) written in Python. The display is created and updated using PyGame, and textures are handled using Pillow. While the rendering is very slow at high resolutions and there are definitely ways to optimize it, PyCaster was mainly created for learning purposes.

## Screenshots
960x540 display (Not recommended - extremely laggy)
![960x540 Screenshot](https://github.com/Jebbly/PyCaster/blob/master/screenshots/Screenshot_1.jpg)

640x360 display (Still relatively laggy)
![640x360 Screenshot](https://github.com/Jebbly/PyCaster/blob/master/screenshots/Screenshot_2.jpg)

## Getting Started
Aside from Python, the only dependencies needed to run PyCaster are [PyGame](https://www.pygame.org/docs/) and [Pillow](https://pillow.readthedocs.io/en/stable/). Both of them can be installed using pip.

To run the raycaster itself, run *raycaster.py*. To adjust the resolution, FOV, or textures, change the constants found in *settings.py*. The resolution should be set very low in order for the renderer to run smoothly.

## Controls
- Use W, A, S, D to move camera
- Use arrow keys to rotate camera
