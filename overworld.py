import pygame
from settings import levels


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, icon_speed):
        super().__init__()
        self.image = pygame.Surface((100, 80))
        self.rect = self.image.get_rect(center = pos)
        self.detection_zone = pygame.Rect(self.rect.centerx-(icon_speed/2),
                                          self.rect.centery-(icon_speed/2),
                                          icon_speed,
                                          icon_speed)

class PlayerIcon(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.Surface((20, 20))
        self.image.fill((0, 0, 255))
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

    # ---------------------------------------------------------
    # Name: setup_nodes
    # Description: Initialzie the overworld
    # ---------------------------------------------------------
    def __setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):
            node_sprite = Node(node_data['node_pos'], self.speed)
            if index <= self.max_level:
                node_sprite.image.fill((255, 0, 0))
            else:
                node_sprite.image.fill((128, 128, 128))
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
        pygame.draw.lines(self.display_surface, (255, 0, 0), False, lines)

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
        self.__draw_path()
        self.input()
        self.update_icon_pos()

        self.nodes.draw(self.display_surface)

        self.icon.update()
        self.icon.draw(self.display_surface)
