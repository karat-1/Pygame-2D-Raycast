import pygame
import math


def raycast(tile_map: dict, target: pygame.Vector2, origin: pygame.Vector2, tile_size: int) -> pygame.Vector2 | bool:
    target_cell = target / tile_size
    vec_ray_start = pygame.Vector2(origin.x / tile_size, origin.y / tile_size)
    vec_ray_dir = (target_cell - vec_ray_start)
    vec_ray_dir = vec_ray_dir.normalize()

    # to account for divide by zero exceptions
    vec_ray_dir.x += 0.000000001
    vec_ray_dir.y += 0.000000001

    vec_ray_stepsize = pygame.Vector2(
        math.sqrt(1 + (vec_ray_dir.y / vec_ray_dir.x) ** 2),
        math.sqrt(1 + (vec_ray_dir.x / vec_ray_dir.y) ** 2)
    )

    vec_map_check = pygame.Vector2(int(vec_ray_start.x), int(vec_ray_start.y))
    vec_ray_length_1d = pygame.Vector2()
    vec_step = pygame.Vector2()

    if vec_ray_dir.x < 0:
        vec_step.x = -1
        vec_ray_length_1d.x = (vec_ray_start.x - vec_map_check.x) * vec_ray_stepsize.x
    else:
        vec_step.x = 1
        vec_ray_length_1d.x = (vec_map_check.x + 1 - vec_ray_start.x) * vec_ray_stepsize.x

    if vec_ray_dir.y < 0:
        vec_step.y = -1
        vec_ray_length_1d.y = (vec_ray_start.y - vec_map_check.y) * vec_ray_stepsize.y
    else:
        vec_step.y = 1
        vec_ray_length_1d.y = (vec_map_check.y + 1 - vec_ray_start.y) * vec_ray_stepsize.y

    tile_found = False
    max_dist = 100
    dist = 0

    while not tile_found and dist < max_dist:
        if vec_ray_length_1d.x < vec_ray_length_1d.y:
            vec_map_check.x += vec_step.x
            dist = vec_ray_length_1d.x
            vec_ray_length_1d.x += vec_ray_stepsize.x
        else:
            vec_map_check.y += vec_step.y
            dist = vec_ray_length_1d.y
            vec_ray_length_1d.y += vec_ray_stepsize.y

        if (int(vec_map_check.x), int(vec_map_check.y)) in tile_map:
            tile_found = True

    if tile_found:
        vec_intersection = vec_ray_start * tile_size + vec_ray_dir * tile_size * dist
        return vec_intersection
    else:
        return False
