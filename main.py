import pygame
import settings
from level import Level
from settings import level_0


pygame.init()
color = pygame.Color(255, 255, 255)
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()
level = Level(level_0, screen, color=color)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill(color)
    level.run()
    pygame.display.update()
    clock.tick(60)
