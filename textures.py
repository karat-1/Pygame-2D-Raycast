import pygame
import numpy as np


class TextureManager:

    def __init__(self, path):
        self.texture = self.get_texture(path)
        self.texture_list = []
        self.__surf_array_list = []
        self.line_cache = {}
        self.scaled_cache = {}  # {texture_index: {column_index: {height: scaled_surface}}}
        self.__heights_to_precompute = range(600, 0, -1)

        self.size = 64

        for i in range(int(self.texture.get_width() // 64)):
            tex = self.texture.subsurface(pygame.Rect(i * 64, 0, 64, 64))
            self.texture_list.append(tex)
            self.__surf_array_list.append(np.transpose(pygame.surfarray.array3d(tex), (1, 0, 2)))
            # self.__surf_array_list.append(pygame.surfarray.array3d(tex))

            line_scans = []
            self.scaled_cache[i] = {}
            for pixel_column in range(64):
                line = tex.subsurface(pygame.Rect(pixel_column, 0, 1, 64))
                line_scans.append(line)

                self.scaled_cache[i][pixel_column] = {}

                for h in self.__heights_to_precompute:
                    scaled_line = pygame.transform.scale(line, (1, h))
                    self.scaled_cache[i][pixel_column][h] = scaled_line

            self.line_cache[i] = line_scans

    @staticmethod
    def get_texture(path, res=(64, 64)) -> pygame.Surface:
        texture = pygame.image.load(path).convert_alpha()
        return texture

    def get_scaled_line(self, texture_index, line_index, height_index):
        return self.scaled_cache[texture_index][line_index][height_index]

    def get_floor_texture(self, texture_index=6):
        return self.__surf_array_list[texture_index]
