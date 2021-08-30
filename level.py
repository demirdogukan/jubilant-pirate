import pygame
import support
from decoration import Cloud, Sky, Water
from tiles import StaticTile, Crate, Coin, Palm, Grass, Tile
from enemy import Enemy
from settings import HEIGHT, TILE_SIZE, WIDTH
from player import Player
from ui import HealthBar, TextLabel, FadingLayout
from interactiveObjects import SilverCoin, GoldenCoin

class Level:
    def __init__(self, level_data, surface, clock=None, color=None):
        # level setup
        self.display_surface = surface
        self.world_shift = -5
        self.current_x = 0
        self.point = 0
        self.display_color = color

        # player and player's goal layout
        player_layout = support.import_csv_file(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        self.collision_counter = 0

        # Import terrain layouts
        terrain_layout = support.import_csv_file(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        crate_layout = support.import_csv_file(level_data["crates"])
        self.crate_sprites = self.create_tile_group(crate_layout, "crates")

        coin_layout = support.import_csv_file(level_data["coins"])
        self.coin_sprites = self.create_tile_group(coin_layout, "coins")

        fg_palms_layout = support.import_csv_file(level_data["fg_palms"])
        self.fg_palms_sprite = self.create_tile_group(fg_palms_layout, "fg_palms")

        bg_palms_layout = support.import_csv_file(level_data["bg_palms"])
        self.bg_palm_sprites = self.create_tile_group(bg_palms_layout, "bg_palms")

        enemy_layout = support.import_csv_file(level_data["enemies"])
        self.enemies_sprite = self.create_tile_group(enemy_layout, "enemies")

        grass_layout = support.import_csv_file(level_data["grass"])
        self.grass_sprite = self.create_tile_group(grass_layout, "grass")

        constraints_layout = support.import_csv_file(level_data["constraints"])
        self.constraints_sprite = self.create_tile_group(constraints_layout, "constraints")

        self.sky = Sky(8)

        level_width = len(terrain_layout[0]) * TILE_SIZE

        self.water = Water(HEIGHT-40, level_width)
        self.cloud = Cloud(400, level_width, 20)

        # UI
        self.hp_bar = HealthBar(TILE_SIZE, (10, 10))
        self.score_lbl = TextLabel(16)
        self.game_over_lbl = TextLabel(64)

        # Collectable Items
        self.silver_coin = SilverCoin(1)
        self.golden_coin = GoldenCoin(2)

        # Fade Layout
        self.fade_layout = FadingLayout()


    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = row_index * TILE_SIZE
                y = col_index * TILE_SIZE
                if col == "0":
                    sprite = Player((x, y), self.display_surface)
                    self.player.add(sprite)

                elif col == "1":
                    hat_surface = pygame.image.load("graphics/character/hat.png").convert_alpha()
                    sprite = StaticTile((x, y), TILE_SIZE, hat_surface)
                    self.goal.add(sprite)

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_tile_group(self, layout, data_name):
        sprites = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                if col != "-1":
                    x = col_index * TILE_SIZE
                    y = row_index * TILE_SIZE

                    if data_name == "terrain":
                        terrain_tile_list = support.import_cut_graphic("graphics/terrain/terrain_tiles.png")
                        tile_surface = terrain_tile_list[int(col)]
                        sprite = StaticTile((x, y), TILE_SIZE, tile_surface)
                        sprites.add(sprite)

                    if data_name == 'crates':
                        sprite = Crate(TILE_SIZE, x, y)
                        sprites.add(sprite)

                    if data_name == 'coins':
                        if col == '0': sprite = Coin(TILE_SIZE, x, y, 'graphics/coins/gold', 'gold')
                        if col == '1': sprite = Coin(TILE_SIZE, x, y, 'graphics/coins/silver', 'silver')
                        sprites.add(sprite)

                    if data_name == 'fg_palms':
                        if col == '0': sprite = Palm(TILE_SIZE, x, y, 'graphics/terrain/palm_small', 5)
                        if col == '1': sprite = Palm(TILE_SIZE, x, y,'graphics/terrain/palm_large')
                        sprites.add(sprite)

                    if data_name == 'bg_palms':
                        sprite = Palm(TILE_SIZE, x,
                                      y, 'graphics/terrain/palm_bg')
                        sprites.add(sprite)

                    if data_name == 'enemies':
                        sprite = Enemy(TILE_SIZE, x, y)
                        sprites.add(sprite)

                    if data_name == 'grass':
                        grass_tile_list = support.import_cut_graphic('graphics/decoration/grass/grass.png')
                        grass_tile_surface = grass_tile_list[int(col)]
                        sprite = Grass(TILE_SIZE, x, y, grass_tile_surface),
                        sprites.add(sprite)

                    if data_name == 'constraints':
                        sprite = Tile((x, y), TILE_SIZE)
                        sprites.add(sprite)

        return sprites

    def enemy_collision_reverse(self):
        for enemy in self.enemies_sprite.sprites():
            if pygame.sprite.spritecollide(enemy,
                                           self.constraints_sprite,
                                           False):
                enemy.reverse()

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < WIDTH / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > WIDTH - (WIDTH / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        collidable_sprites = self.terrain_sprites.sprites() + self.fg_palms_sprite.sprites() + self.crate_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if ((player.on_left) and
                (player.rect.left < self.current_x) or
                (player.direction.x >= 0)):
            player.on_left = False

        if ((player.on_right) and
                (player.rect.right > self.current_x) or
                (player.direction.x <= 0)):
            player.on_right = False

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        collidable_sprites = self.terrain_sprites.sprites() + self.fg_palms_sprite.sprites() + self.crate_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground:
            if player.direction.y < 0 or player.direction.y > 1:
                player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def enemy_collision(self):
        player = self.player.sprite
        enemy_sprite = self.enemies_sprite.sprites()
        for sprite in enemy_sprite:
            if sprite.rect.colliderect(player.rect):
                self.take_damage(player, sprite.enemy_damage)
                break

    def take_damage(self, player, damage_amount):
        if self.is_game_over() is False:
            player.health = max(player.health-damage_amount, 0)
            print(player.health)
            self.hp_bar.fade(damage_amount)

    def is_game_over(self):
        player = self.player.sprite
        return True if player.health <= 0 else False

    def coin_collision(self):
        player = self.player.sprite
        coin_sprites = self.coin_sprites.sprites()
        text = None
        for sprite in coin_sprites:
            if sprite.rect.colliderect(player.rect):
                if sprite.type == "gold":
                    self.point += self.golden_coin.point
                    text =  self.golden_coin.Get_Text()
                    sprite.kill()

                elif sprite.type == "silver":
                    self.point += self.silver_coin.point
                    text = self.silver_coin.Get_Text()
                    sprite.kill()

        return text if text is not None else f"SCORE: {self.point}"

    def water_collision(self):
        player = self.player.sprite
        water_sprite = self.water.water_sprites.sprites()
        for sprite in water_sprite:
            if sprite.rect.colliderect(player.rect):
                self.take_damage(player, 100)
                break

    def run(self):

        # level tiles
        self.sky.draw(self.display_surface)

        self.cloud.draw(self.display_surface, self.world_shift)

        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        self.grass_sprite.update(self.world_shift)
        self.grass_sprite.draw(self.display_surface)

        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)
        self.crate_sprites.draw(self.display_surface)

        self.crate_sprites.update(self.world_shift)

        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        self.fg_palms_sprite.update(self.world_shift)
        self.fg_palms_sprite.draw(self.display_surface)

        self.enemies_sprite.update(self.world_shift)
        self.constraints_sprite.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemies_sprite.draw(self.display_surface)

        self.water.draw(self.display_surface, self.world_shift)
        self.water_collision()

        # UI
        self.hp_bar.draw(self.display_surface)

        point_txt = self.coin_collision()
        self.score_lbl.draw(point_txt,
                           self.display_surface,
                           (64, 64))

        # Enemy
        if self.collision_counter > 1:
            self.enemy_collision()
            self.collision_counter = 0
        self.collision_counter += 0.20

        # Player Goal
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # player
        self.player.update()
        self.player.draw(self.display_surface)
        self.scroll_x()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()

        # Game Over
        if self.is_game_over():
            self.fade_layout.start_fading()
            self.fade_layout.draw(self.display_surface)
            self.game_over_lbl.draw("GAME OVER",
                                     self.display_surface,
                                     ((WIDTH-self.game_over_lbl.get_width())/2,
                                     (HEIGHT-self.game_over_lbl.get_height())/2))

        self.fade_layout.update(self.world_shift)