import pygame
from pygame.version import PygameVersion
from settings import TILE_SIZE, WIDTH, HEIGHT


class HealthBar(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        super().__init__()

        self.size = size
        self.start_x = 10
        self.start_y = 10
        self.pos = pos

        self.ui_end = pygame.image.load("graphics/ui/ui_end.png").convert_alpha()
        self.ui_middle = pygame.image.load("graphics/ui/ui_middle.png").convert_alpha()
        self.ui_start = pygame.image.load("graphics/ui/ui_start.png").convert_alpha()

        self.max_size_x = self.prev_max_size = TILE_SIZE * 2 + 26
        self.max_size_y = 5

        self.image  = pygame.Surface((self.max_size_x, self.max_size_y))
        self.image.fill((220, 73, 73))
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, surface):
        surface.blit(self.ui_start, (self.start_x, self.start_y))
        surface.blit(self.ui_middle, (self.start_x + self.size, self.start_y))
        surface.blit(self.ui_end, (self.start_x + self.size * 2, self.start_y))

        surface.blit(self.image, (self.start_x + self.size / 2, 38))

    def fade(self, damage):
        fade_amount = self.__normalize_number(damage, self.prev_max_size)
        self.max_size_x -= fade_amount
        max_value = max(self.max_size_x, 0.1)
        self.image = pygame.Surface((max_value, self. max_size_y))
        self.image.fill((220, 73, 73))
        self.rect = self.image.get_rect(center=self.pos)

    def __normalize_number(self, number, norm):
        return number * (norm / 100)


class TextLabel:
    def __init__(self, font_size):
        self.font_size = font_size
        self.arcade_font = pygame.font.Font("graphics/ARCADEPI.TTF", self.font_size)
        self.text_img = self.arcade_font.render("", False, (0, 0, 0))

    def draw(self, text, surface, pos):
        self.text_img = self.arcade_font.render(text, False, (0, 0, 0))
        surface.blit(self.text_img, pos)

    def get_width(self): return self.text_img.get_width()
    def get_height(self): return self.text_img.get_height()


class FadingLayout(pygame.sprite.Sprite):
    def __init__(self):
        self.fadingSurface = pygame.Surface((WIDTH, HEIGHT))
        self.color = pygame.Color(255, 255, 255)
        self.fadingSurface.set_colorkey(self.color)

        self.alpha = 0
        self.fading_amount = 2

        self.rect = self.fadingSurface.get_rect()

    def update(self, x_shift):
        self.rect.x += x_shift

    def draw(self, screen):
        screen.blit(self.fadingSurface, (0, 0))

    # ---------------------------------------------------------
    # Name: fade_screen
    # Description: right after the player has died, the screen will process fading
    # ---------------------------------------------------------
    def start_fading(self):
        self.alpha = min(255, self.alpha + self.fading_amount)
        self.fadingSurface.set_alpha(self.alpha)

        return self.alpha == 255


    def get_color(self):
        return self.color

    def set_color(self, color):
        self.color = color

