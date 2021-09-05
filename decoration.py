from support import import_folder
from tiles import AnimatedTile, StaticTile
from settings import HEIGHT, WIDTH, vertical_tile_size, TILE_SIZE
from random import choice, randint, random
import pygame


class Sky:
    def __init__(self, horizon, style = 'level'):
        self.top = pygame.image.load("graphics/decoration/sky/sky_top.png").convert()
        self.middle = pygame.image.load("graphics/decoration/sky/sky_middle.png").convert()
        self.bottom = pygame.image.load("graphics/decoration/sky/sky_bottom.png").convert()

        self.horizon = horizon

        # Stretch the surface
        self.top = pygame.transform.scale(self.top, (WIDTH, TILE_SIZE))
        self.middle = pygame.transform.scale(self.middle, (WIDTH, TILE_SIZE))
        self.bottom = pygame.transform.scale(self.bottom, (WIDTH, TILE_SIZE))

        self.style = style
        if self.style == "overworld":
            palm_surfaces = import_folder("graphics/overworld/palms")
            self.palms = []

            for palm_surf in [choice(palm_surfaces) for i in range(10)]:
                x = randint(0, WIDTH)
                y = self.horizon * TILE_SIZE + randint(50, 100)
                rect = palm_surf.get_rect(midbottom=(x, y))
                self.palms.append((palm_surf, rect))

    def draw(self, surface):
        for row in range(vertical_tile_size):
            y = row * TILE_SIZE
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            elif row > self.horizon:
                surface.blit(self.bottom, (0, y))

            if self.style == "overworld":
                for palm in self.palms:
                    surface.blit(palm[0], palm[1])

class Water:
    def __init__(self, top, level_width):
        water_start = -WIDTH
        water_tile_width = 192
        tile_x_amount = int((level_width + WIDTH) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start
            y = top

            sprite = AnimatedTile(water_tile_width, x, y, "graphics/decoration/water")
            self.water_sprites.add(sprite)

    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)


class Cloud:
    def __init__(self, horizon, level_width ,cloud_number):
        self.cloud_surface_list = import_folder("graphics/decoration/clouds")

        self.max_x = level_width + HEIGHT
        self.min_x = -HEIGHT

        self.max_y = horizon
        self.min_y = 0

        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            rand_cloud_surface = choice(self.cloud_surface_list)

            rand_x = randint(self.min_x, self.max_x)
            rand_y = randint(self.min_y, self.max_y)

            cloud_sprite = StaticTile((rand_x, rand_y), 0, rand_cloud_surface)
            self.cloud_sprites.add(cloud_sprite)

    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)


