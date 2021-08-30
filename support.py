import pygame
from os import walk
from csv import reader


def import_folder(full_path):
    surface_list = []
    for _, __, img_file in walk(full_path):
        for image in img_file:
            img_path = full_path + '/' + image
            img_surf = pygame.image.load(img_path).convert_alpha()
            surface_list.append(img_surf)

    return surface_list


def import_cut_graphic(path, tile_width=64, tile_height=64):
    surface = pygame.image.load(path).convert_alpha()
    title_num_x = int(surface.get_size()[0] / tile_width)
    title_num_y = int(surface.get_size()[1] / tile_height)
    cut_tiles = []

    for row in range(title_num_y):
        for col in range(title_num_x):
            x = col * tile_width
            y = row * tile_height
            new_surf = pygame.Surface((tile_width, tile_height),
                                      flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, 64, 64))
            cut_tiles.append(new_surf)

    return cut_tiles


def import_csv_file(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=",")
        for row in level:
            terrain_map.append(list(row))

        return terrain_map
