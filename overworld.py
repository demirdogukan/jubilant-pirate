from decoration import Sky
import pygame
from support import import_folder
from settings import levels


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, icon_speed, path, status):
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        self.detection_zone = pygame.Rect(self.rect.centerx-(icon_speed/2),
                                          self.rect.centery-(icon_speed/2),
                                          icon_speed,
                                          icon_speed)

        self.status = status

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index > len(self.frames):
            self.frame_index = 0

        self.image = self.frames[int(self.frame_index)]

    def update(self):
        if self.status == "available":
            self.animate()
        else:
            tint_surface = self.image.copy()
            tint_surface.fill((0, 0, 0), None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tint_surface, (0, 0))

class PlayerIcon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load("graphics/overworld/hat.png").convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        self.rect.center = self.pos


class OverWorld:
    def __init__(self, start_level, max_level, surface, create_level):
        self.max_level = max_level
        self.current_level = start_level
        self.display_surface = surface
        self.create_level = create_level

        # Movement Logic
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 4

        # flags
        self.isMoving = False

        # sprite
        self.__setup_nodes()
        self.__setup_player_icon()

        self.sky = Sky(8, "overworld")

    # ---------------------------------------------------------
    # Name: setup_nodes
    # Description: Initialzie the overworld
    # ---------------------------------------------------------
    def __setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], self.speed, node_data["node_graphics"], "available")
            else:
                node_sprite = Node(node_data['node_pos'], self.speed, node_data["node_graphics"], "locked")
            self.nodes.add(node_sprite)

    def __setup_player_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        sprite = PlayerIcon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(sprite)

    # ---------------------------------------------------------
    # Name:draw_path
    # Description: draws a line between nodes
    # ---------------------------------------------------------
    def __draw_path(self):
        lines = [lvl['node_pos'] for key, lvl in levels.items() if key <= self.max_level]
        pygame.draw.lines(self.display_surface, (220, 73, 73), False, lines, 6)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.isMoving:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data("next")
                self.current_level += 1
                self.isMoving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data("previous")
                self.current_level -= 1
                self.isMoving = True
            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def get_movement_data(self, target):
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == "next":
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        elif target == "previous":
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()

    def update_icon_pos(self):
        if self.move_direction and self.isMoving:
            self.icon.sprite.pos += self.move_direction * self.speed
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.isMoving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def run(self):
        self.sky.draw(self.display_surface)

        self.__draw_path()
        self.input()
        self.update_icon_pos()

        self.nodes.draw(self.display_surface)
        self.nodes.update()

        self.icon.update()
        self.icon.draw(self.display_surface)
