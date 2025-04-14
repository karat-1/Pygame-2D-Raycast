import pygame


class TextureManager:

    def __init__(self, path):
        self.texture = self.get_texture(path)
        self.texture_list = []
        self.line_cache = {}
        self.scaled_cache = {}  # {texture_index: {column_index: {height: scaled_surface}}}
        self.__heights_to_precompute = range(320, 0, -1)

        self.size = 64

        for i in range(int(self.texture.get_width() // 64)):
            tex = self.texture.subsurface(pygame.Rect(i * 64, 0, 64, 64))
            self.texture_list.append(tex)

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