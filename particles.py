from support import import_folder
import pygame


class Particle(pygame.sprite.Sprite):

    def __init__(self, path, pos):
        super().__init__()
        self.frame_index = 0
        self.frame_amount = 0.50

        self.frames = import_folder(path)
        self.image = self.frames[self.frame_index]

        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.frame_amount
        if self.frame_index >= len(self.frames):
            # Destroy sprite itself
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, shift=0):
        self.animate()
        self.rect.x += shift


class ExplosionParticle(Particle):
    def __init__(self, pos):
        self._path = "graphics/enemy/explosion"
        super().__init__(self._path, pos)

    def update(self, shift): return super().update(shift)
