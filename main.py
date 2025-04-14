import math
from textures import TextureManager
import pygame
from numba import njit
import numpy as np

pygame.init()  # Start Pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
GAME_WIDTH, GAME_HEIGHT = 320, 180
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))  # The low-res surface
abstract_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
RENDER_MODE = 1
pygame.display.set_caption('2D Raycast Demo')
clock = pygame.time.Clock()
clock.tick(60)
f_key_pressed = False
tile_size = 32
tile_grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 0, 0, 0, 5, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
tile_grid_np = np.array(tile_grid, dtype=np.int32)

mouse_pos = None
player = pygame.Vector2(2 * 32, 2 * 32)
player_dir = pygame.Vector2(1, 0)
plane = pygame.Vector2(0, 0.60)
rot_speed = 1
vel = 150
dt = 0
target_fps = 60
pygame.mouse.get_focused()
collision_point = pygame.Vector2(0, 0)
render_color = False
textures = TextureManager('resources/wolftextures.png')
line_buffer = []


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


class Tile:
    def __init__(self, color, pos, rect=None):
        self.color = color
        self.rect = rect
        self.pos = pos  # as in cell position, not pixel position


def render_topdown():
    for y, row in enumerate(tile_grid):
        for x, column in enumerate(row):
            color = None
            match tile_grid[y][x]:
                case 1:
                    color = pygame.Color('red')
                case 2:
                    color = pygame.Color('green')
                case 3:
                    color = pygame.Color('blue')
                case 4:
                    color = pygame.Color('white')
                case _:
                    color = pygame.Color('yellow')  # default
            pygame.draw.rect(abstract_surface, color, pygame.Rect(x * 32, y * 32, 32, 32))

    pygame.draw.circle(abstract_surface, (255, 90, 90), player, 16)

    pygame.draw.line(abstract_surface, (0, 0, 0), player, player + player_dir * 200)
    pygame.transform.scale_by(abstract_surface, (1, 1), screen)


@njit
def raycast_column(
        x: int,
        player_x: float,
        player_y: float,
        dir_x: float,
        dir_y: float,
        plane_x: float,
        plane_y: float,
        tile_grid: np.ndarray,
        tile_size: int,
        game_width: int,
        game_height: int
):
    camera_x = 2 * x / game_width - 1
    raydir_x = dir_x + plane_x * camera_x
    raydir_y = dir_y + plane_y * camera_x

    map_x = int(player_x) // tile_size
    map_y = int(player_y) // tile_size
    player_tile_x = player_x / tile_size
    player_tile_y = player_y / tile_size

    delta_dist_x = 1e30 if raydir_x == 0 else abs(1 / raydir_x)
    delta_dist_y = 1e30 if raydir_y == 0 else abs(1 / raydir_y)

    if raydir_x < 0:
        step_x = -1
        side_dist_x = (player_tile_x - map_x) * delta_dist_x
    else:
        step_x = 1
        side_dist_x = (map_x + 1 - player_tile_x) * delta_dist_x

    if raydir_y < 0:
        step_y = -1
        side_dist_y = (player_tile_y - map_y) * delta_dist_y
    else:
        step_y = 1
        side_dist_y = (map_y + 1 - player_tile_y) * delta_dist_y

    hit = False
    side = 0

    while not hit:
        if side_dist_x < side_dist_y:
            side_dist_x += delta_dist_x
            map_x += step_x
            side = 0
        else:
            side_dist_y += delta_dist_y
            map_y += step_y
            side = 1

        if tile_grid[map_y, map_x] != 0:
            hit = True

    if side == 0:
        perp_wall_dist = side_dist_x - delta_dist_x
    else:
        perp_wall_dist = side_dist_y - delta_dist_y

    line_height = int(game_height / max(perp_wall_dist, 0.0001))
    draw_start = int(game_height / 2 - line_height / 2)
    draw_start = max(draw_start, -10000)  # no clamping here
    draw_end = int(game_height / 2 + line_height / 2)
    draw_height = int(draw_end - draw_start)

    if side == 0:
        hit_pos = player_tile_y + (map_x - player_tile_x + (1 - step_x) / 2) / raydir_x * raydir_y
    else:
        hit_pos = player_tile_x + (map_y - player_tile_y + (1 - step_y) / 2) / raydir_y * raydir_x

    wall_x = hit_pos - math.floor(hit_pos)
    tex_x = int(wall_x * 64)

    if side == 0 and raydir_x > 0:
        tex_x = 64 - tex_x - 1
    if side == 1 and raydir_y < 0:
        tex_x = 64 - tex_x - 1

    tex_x = max(0, min(63, tex_x))
    draw_height = max(1, min(draw_height, 600))

    return tex_x, map_x, map_y, draw_start, draw_height, side


def render_raycasted_view():
    for x in range(GAME_WIDTH):
        tex_x, map_x, map_y, draw_start, draw_height, side = raycast_column(
            x,
            player.x,
            player.y,
            player_dir.x,
            player_dir.y,
            plane.x,
            plane.y,
            tile_grid_np,  # muss ein np.ndarray[int32] sein
            tile_size,
            GAME_WIDTH,
            GAME_HEIGHT
        )
        draw_rect = textures.get_scaled_line(tile_grid[map_y][map_x], tex_x, draw_height)
        game_surface.blit(draw_rect, (x, draw_start))
        draw_rect = textures.get_scaled_line(tile_grid[map_y][map_x], tex_x, draw_height)
        line_buffer.append([draw_rect, (x, draw_start)])


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Stop running

    move_speed = vel * dt
    rt_speed = rot_speed * dt
    # Basic code for input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        old_dir_x = player_dir.x
        player_dir.x = player_dir.x * math.cos(rt_speed) - player_dir.y * math.sin(rt_speed)
        player_dir.y = old_dir_x * math.sin(rt_speed) + player_dir.y * math.cos(rt_speed)
        old_plane = plane
        plane.x = plane.x * math.cos(rt_speed) - plane.y * math.sin(rt_speed)
        plane.y = old_plane.x * math.sin(rt_speed) + plane.y * math.cos(rt_speed)

    if keys[pygame.K_a]:
        old_dir_x = player_dir.x
        player_dir.x = player_dir.x * math.cos(-rt_speed) - player_dir.y * math.sin(-rt_speed)
        player_dir.y = old_dir_x * math.sin(-rt_speed) + player_dir.y * math.cos(-rt_speed)
        old_plane = plane
        plane.x = plane.x * math.cos(-rt_speed) - plane.y * math.sin(-rt_speed)
        plane.y = old_plane.x * math.sin(-rt_speed) + plane.y * math.cos(-rt_speed)

    if keys[pygame.K_w]:
        next_x = player.x + player_dir.x * move_speed
        next_y = player.y + player_dir.y * move_speed

        # X-Kollision (Y bleibt gleich)
        if not tile_grid[int(player.y) // tile_size][int(next_x) // tile_size]:
            player.x = next_x

        # Y-Kollision (X ist ggf. schon aktualisiert)
        if not tile_grid[int(next_y) // tile_size][int(player.x) // tile_size]:
            player.y = next_y

    if keys[pygame.K_s]:
        next_x = player.x - player_dir.x * move_speed
        next_y = player.y - player_dir.y * move_speed

        if not tile_grid[int(player.y) // tile_size][int(next_x) // tile_size]:
            player.x = next_x

        if not tile_grid[int(next_y) // tile_size][int(player.x) // tile_size]:
            player.y = next_y

    if keys[pygame.K_f]:
        if not f_key_pressed:
            RENDER_MODE = not RENDER_MODE
            f_key_pressed = True
    else:
        f_key_pressed = False

    if RENDER_MODE == 0:
        render_topdown()
        # render topdown view for debugging
    elif RENDER_MODE == 1:
        render_raycasted_view()
        game_surface.blits(line_buffer)
        line_buffer.clear()
        pygame.transform.scale_by(game_surface, (SCREEN_WIDTH // GAME_WIDTH, SCREEN_HEIGHT // GAME_HEIGHT), screen)
        # screen.blit(game_surface)

    dt = clock.tick(0) / 1000.0
    dt = min(max(0.0001, dt), 1)
    pygame.display.update()
    abstract_surface.fill('#124e89')
    game_surface.fill('#000000')
    pygame.display.set_caption(f'Raycasting - {int(clock.get_fps())}fps')

pygame.quit()  # Close the window
