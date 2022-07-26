import pygame
import math
from line2d_raycast import Line

pygame.init()  # Start Pygame

screen = pygame.display.set_mode((1280, 720))  # Start the screen
pygame.display.set_caption('2D Raycast Demo')
clock = pygame.time.Clock()
clock.tick(60)

tile_size = 32
map_width = 1280 // tile_size
map_height = 720 // tile_size
tile_grid = {}
mouse_pos = None
raycast_line = Line(0, 0, 0, 0)
player = pygame.Vector2(0, 0)
vel = 10
dt = 0
target_fps = 60
exampleLine = Line(800, 0, 800, 720)


class Tile:
    def __init__(self, color, pos, rect=None):
        self.color = color
        self.rect = rect
        self.pos = pos  # as in cell position, not pixel position


def create_tile(pos):
    x_pos = pos[0] // tile_size
    y_pos = pos[1] // tile_size
    tile_grid[(x_pos, y_pos)] = Tile((0, 125, 150), (x_pos, y_pos))


def delete_tile(pos):
    x_pos = pos[0] // tile_size
    y_pos = pos[1] // tile_size
    del (tile_grid[(x_pos, y_pos)])


for i in range(2, 16):
    create_tile((i * tile_size, 64))
    create_tile((i * tile_size, 512))

for i in range(2, 16):
    create_tile((64, i * tile_size))
    create_tile((496, i * tile_size))

tile_grid_old = len(tile_grid)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # The user closed the window!
            running = False  # Stop running
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                create_tile(mouse_pos)
            if event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                try:
                    delete_tile(mouse_pos)
                except Exception as e:
                    print(e)

    # Basic code for input
    keys = pygame.key.get_pressed()
    mouse_pos = (pygame.Vector2(pygame.mouse.get_pos()))
    if keys[pygame.K_a]:
        player.x -= vel * dt

    if keys[pygame.K_d]:
        player.x += vel * dt

    if keys[pygame.K_w]:
        player.y -= vel * dt

    if keys[pygame.K_s]:
        player.y += vel * dt

    # the line object needs to be updated before usage.
    # Does not need to be each frame but before calling its methods
    raycast_line.update(player.x, player.y, mouse_pos.x, mouse_pos.y)

    # shooting the raycast
    collision_point = raycast_line.raycast(tile_grid, pygame.Vector2(mouse_pos), tile_size)

    screen.fill((30, 29, 57))

    for tile in tile_grid:
        tile = tile_grid[tile]
        pygame.draw.rect(screen, tile.color,
                         pygame.Rect(tile.pos[0] * tile_size, tile.pos[1] * tile_size, tile_size, tile_size))
    pygame.draw.circle(screen, (255, 90, 90), player, 16)

    # checking if there is anything in our collision point
    if collision_point:
        pygame.draw.circle(screen, (255, 255, 255), collision_point, 8, 1)

    # checking if we intersect with the red example line
    if raycast_line.collideline(exampleLine.start_point, exampleLine.end_point):
        pygame.draw.aaline(screen, (255, 0, 0), exampleLine.start_point, exampleLine.end_point)
    else:
        pygame.draw.aaline(screen, (255, 255, 0), exampleLine.start_point, exampleLine.end_point)

    pygame.draw.aaline(screen, (0, 255, 0), raycast_line.start_point, raycast_line.end_point)

    dt = clock.tick(65) * .001 * target_fps
    pygame.display.update()

pygame.quit()  # Close the window
