from sys import path
from support import import_folder
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift=0):
        self.rect.x += x_shift


class StaticTile(Tile):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size)
        self.image = surface


class Crate(StaticTile):
    def __init__(self, size, x, y):
        super().__init__((x, y),
                         size,
                         pygame.image.load("graphics/terrain/crate/crate.png").convert_alpha())
        offset_y = size + y
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class Grass(StaticTile):
    def __init__(self, size, x, y, surface):
        super().__init__((x, y), size, surface)


class AnimatedTile(Tile):
    def __init__(self, size, x, y, path):
        super().__init__((x, y), size)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift=0):
        self.animate()
        self.rect.x += shift


class Coin(AnimatedTile):
    def __init__(self, size, x, y, path, coin_type):
        super().__init__(size, x, y, path)
        center_x = size / 2
        center_y = size / 2
        self.image.get_rect(bottomleft=(center_x, center_y))
        self.type = coin_type

class Palm(AnimatedTile):
    def __init__(self, size, x, y, path, offset_y = 0):
        super().__init__(size, x, y, path)
        offset_y = y - offset_y
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))

