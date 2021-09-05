import pygame
import settings
from level import Level
from overworld import OverWorld

class Game:
    def __init__(self):
        self.max_level = 3
        self.overworld = OverWorld(0, self.max_level, screen, self.create_level)
        self.status = "overworld"

    def create_level(self, current_level):
        self.level = Level(screen, current_level, self.create_overworld)
        self.status = "level"

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = OverWorld(current_level, self.max_level, screen, self.create_level)
        self.status = "overworld"

    def run(self):
        if self.status == "overworld":
            self.overworld.run()
        else:
            self.level.run()

pygame.init()
color = pygame.Color(128, 128, 128)
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill(color)
    game.run()
    pygame.display.update()
    clock.tick(60)
