import math
from textures import TextureManager
import pygame

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


def render_raycasted_view():
    for x in range(GAME_WIDTH):
        camera_x = 2 * x / GAME_WIDTH - 1
        raydir = pygame.Vector2(player_dir.x + plane.x * camera_x,
                                player_dir.y + plane.y * camera_x)
        map_x = int(player.x) // tile_size
        map_y = int(player.y) // tile_size
        player_tile = player / tile_size

        side_dist = pygame.Vector2(0, 0)

        delta_dist_x = 1e30 if raydir.x == 0 else abs(1 / raydir.x)
        delta_dist_y = 1e30 if raydir.y == 0 else abs(1 / raydir.y)

        perp_wall_dist = 0

        step_x = 0
        step_y = 0

        hit = False
        side = None

        if raydir.x < 0:
            step_x = -1
            side_dist.x = (player_tile.x - map_x) * delta_dist_x
        else:
            step_x = 1
            side_dist.x = (map_x + 1 - player_tile.x) * delta_dist_x

        if raydir.y < 0:
            step_y = -1
            side_dist.y = (player_tile.y - map_y) * delta_dist_y
        else:
            step_y = 1
            side_dist.y = (map_y + 1 - player_tile.y) * delta_dist_y

        while not hit:
            if side_dist.x < side_dist.y:
                side_dist.x += delta_dist_x
                map_x += step_x
                side = 0
            else:
                side_dist.y += delta_dist_y
                map_y += step_y
                side = 1
            if tile_grid[map_y][map_x]:
                hit = True
        if side == 0:
            perp_wall_dist = (side_dist.x - delta_dist_x)
        else:
            perp_wall_dist = (side_dist.y - delta_dist_y)

        line_height = round(GAME_HEIGHT / perp_wall_dist)
        draw_start = int(-line_height / 2 + GAME_HEIGHT / 2)
        if draw_start < 0:
            draw_start = 0
        draw_end = line_height / 2 + GAME_HEIGHT / 2
        if draw_end >= GAME_HEIGHT:
            draw_end = GAME_HEIGHT - 1

        if side == 0:
            hit_pos = player.y / tile_size + (map_x - player.x / tile_size + (1 - step_x) / 2) / raydir.x * raydir.y
        else:
            hit_pos = player.x / tile_size + (map_y - player.y / tile_size + (1 - step_y) / 2) / raydir.y * raydir.x

        wall_x = hit_pos - math.floor(hit_pos)
        tex_x = int(wall_x * 64)

        # Beispiel: nur jede 2. Spalte auf entfernten Wänden
        if line_height < 20:
            tex_x = (tex_x // 2) * 2

        if side == 0 and raydir.x > 0:
            tex_x = 64 - tex_x - 1
        if side == 1 and raydir.y < 0:
            tex_x = 64 - tex_x - 1


        if render_color:
            match tile_grid[map_y][map_x]:
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
            if side == 1:
                color = pygame.Color(color.r // 2, color.g // 2, color.b // 2)
            pygame.draw.rect(game_surface, color, pygame.Rect(x, draw_start, 1, abs(draw_start - draw_end)))
        else:
            draw_height = int(draw_end - draw_start + 0.5)
            draw_height = clamp(draw_height, 1, 320)
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
        pygame.transform.scale_by(game_surface, (4, 4), screen)
        # screen.blit(game_surface)

    dt = clock.tick(0) / 1000.0
    dt = min(max(0.0001, dt), 1)
    pygame.display.update()
    abstract_surface.fill('#124e89')
    game_surface.fill('#000000')
    pygame.display.set_caption(f'Raycasting - {int(clock.get_fps())}fps')

pygame.quit()  # Close the window
