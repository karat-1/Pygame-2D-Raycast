# Pygame-2D-Raycast
A module which provides some basic and useful raycasting functionalities such as:
- checking collisions with a rectangle
- checking collisions with a line
- checking collisions with a full tilemap

## How to use
Import the line2d_raycast Line class into your project
```py
from line2d_raycast import Line
```

Instantiate a line object:
```py
raycast_line = Line(0, 0, 0, 0)
exampleLine = Line(800, 0, 800, 720)
```

If you give the line object to a moving entity such as an enemy 
do not forget to update it during your entities update loop via:
```py
raycast_line.update(x1, y1, x2, y2)
```

check for collisions via:
```py
collision_point = raycast_line.raycast(tile_grid, pygame.Vector2(mouse_pos), tile_size)
```
or
```py
if raycast_line.collideline(exampleLine.start_point, exampleLine.end_point):
    pygame.draw.aaline(screen, (255, 0, 0), exampleLine.start_point, exampleLine.end_point)
else:
    pygame.draw.aaline(screen, (255, 255, 0), exampleLine.start_point, exampleLine.end_point)
```
