import pygame
import math
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        # Health
        self.health = 100

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

        self.invisible_amount = 400
        self.is_invisible = False
        self.start_invisible_time = 0

        # Surface
        self.display_surface = surface

    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
        self.__invisible_timer()

        # pygame.draw.rect(self.display_surface, (255, 0, 0), self.rect)

    def import_character_assets(self):
        path = "graphics/character/"
        self.animations = {"idle": [], "run": [], "jump": [], "fall": []}
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self):
        animation = self.animations[self.status]
        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

        # make player invisible when taking damage
        if self.is_invisible:
            value = self.__wave_value()
            self.image.set_alpha(value)
        else:
            self.image.set_alpha(255)

        # Set player's collider
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)
        else:
            self.rect = self.image.get_rect(center=self.rect.center)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > self.gravity:
            self.status = "fall"
        else:
            if self.direction.x != 0:
                self.status = "run"
            else:
                self.status = "idle"

    def jump(self):
        self.direction.y = self.jump_speed

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def __wave_value(self):
        return 255 if math.sin(pygame.time.get_ticks()) >= 0 else 0

    def take_damage(self, damage_amount):
        if not self.is_invisible:
            self.health = max(self.health-damage_amount, 0)
            self.is_invisible = True
            self.start_invisible_time = pygame.time.get_ticks()

    def __invisible_timer(self):
        if self.is_invisible:
            end_invisible_time = pygame.time.get_ticks()
            if end_invisible_time - self.start_invisible_time > self.invisible_amount:
                self.is_invisible = False
