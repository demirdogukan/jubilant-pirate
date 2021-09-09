import pygame
import support
from particles import ExplosionParticle
from decoration import Cloud, Sky, Water
from tiles import StaticTile, Crate, Coin, Palm, Grass, Tile
from enemy import Enemy
from settings import HEIGHT, TILE_SIZE, WIDTH
from player import Player
from ui import HealthBar, TextLabel, FadingLayout
from interactiveObjects import SilverCoin, GoldenCoin
from overworld import levels


class Level:
    def __init__(self, surface, current_level, create_overworld):
        # level setup
        self.display_surface = surface
        self.world_shift = -5
        self.current_x = 0
        self.point = 0

        self.current_level = current_level
        self.create_overworld = create_overworld
        self.level_data = levels[self.current_level]
        self.new_max_level = self.level_data["unlock"]

        # player and player's goal layout setup
        player_layout = support.import_csv_file(self.level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.is_goal_achieved = False
        self.goal = pygame.sprite.Group()
        self.collision_counter = 0

        self.player_setup(player_layout)
        self.import_layouts()

    def import_layouts(self):

        # Import terrain layouts
        terrain_layout = support.import_csv_file(self.level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        crate_layout = support.import_csv_file(self.level_data["crates"])
        self.crate_sprites = self.create_tile_group(crate_layout, "crates")

        coin_layout = support.import_csv_file(self.level_data["coins"])
        self.coin_sprites = self.create_tile_group(coin_layout, "coins")

        fg_palms_layout = support.import_csv_file(self.level_data["fg_palms"])
        self.fg_palms_sprite = self.create_tile_group(fg_palms_layout, "fg_palms")

        bg_palms_layout = support.import_csv_file(self.level_data["bg_palms"])
        self.bg_palm_sprites = self.create_tile_group(bg_palms_layout, "bg_palms")

        enemy_layout = support.import_csv_file(self.level_data["enemies"])
        self.enemies_sprite = self.create_tile_group(enemy_layout, "enemies")

        grass_layout = support.import_csv_file(self.level_data["grass"])
        self.grass_sprite = self.create_tile_group(grass_layout, "grass")

        constraints_layout = support.import_csv_file(self.level_data["constraints"])
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

        # Particles
        self.explosion_sprite = pygame.sprite.Group()

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE
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
        # ---------------------------------------------------------
        # Name: scroll_x
        # Description: it makes the screen move to opposite direction of the player
        # when player moves to the right, the all objects in the screen moves to left
        # so that player moves to right in a way
        # ---------------------------------------------------------
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        # when player moves to left all objects in the scene moves to right
        if player_x < WIDTH / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        # whereas player moves to right, objects in the scene moves to left
        elif player_x > WIDTH - (WIDTH / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        # if the player doesn't cross the boundary, the objects can stay in same position
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
        self.invisible_end = 0
        # Get enemy sprites colliding with player's
        enemy_sprites = pygame.sprite.spritecollide(player, self.enemies_sprite, False)

        for enemy in enemy_sprites:
            player_bottom = player.rect.bottom
            enemy_mid = enemy.rect.centery
            enemy_top  = enemy.rect.top
            # kill the enemy
            if enemy_top < player_bottom < enemy_mid and player.direction.y >= 0:
                # draw explosion
                particle = ExplosionParticle(enemy.rect.center)
                self.explosion_sprite.add(particle)
                player.direction.y = -15
                enemy.kill()
            else:
                player.take_damage(enemy.enemy_damage)

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
                player.take_damage(100)

    def input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            self.create_overworld(self.current_level, self.new_max_level)
        elif key[pygame.K_ESCAPE]:
            self.create_overworld(self.current_level, 0)

    def goal_collision(self):
        player_sprite = self.player.sprite
        goal_sprite = self.goal.sprites()
        for sprite in goal_sprite:
            if sprite.rect.colliderect(player_sprite.rect) and not self.is_goal_achieved:
                self.get_to_next_level()

    def get_to_next_level(self):
        self.is_goal_achieved = True
        self.current_level += 1
        self.create_overworld(self.current_level, self.current_level + 1)

    def end_the_game(self):
            is_fading_done = self.fade_layout.start_fading()
            self.fade_layout.draw(self.display_surface)
            self.game_over_lbl.draw("GAME OVER",
                                     self.display_surface,
                                     ((WIDTH-self.game_over_lbl.get_width())/2,
                                     (HEIGHT-self.game_over_lbl.get_height())/2))

            if is_fading_done:
                self.create_overworld(self.current_level, self.current_level)

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

        # Player Goal
        self.goal.draw(self.display_surface)
        self.goal.update(self.world_shift)
        # UI
        self.hp_bar.draw(self.display_surface)
        self.hp_bar.fade(self.player.sprite.health)
        point_txt = self.coin_collision()
        self.score_lbl.draw(point_txt,
                           self.display_surface,
                           (64, 64))

        # Enemy
        if self.collision_counter > 1:
            self.enemy_collision()
            self.collision_counter = 0
        self.collision_counter += 0.20

        # player
        self.player.update()
        self.player.draw(self.display_surface)
        self.scroll_x()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()

        # Game Over
        if self.is_game_over():
            self.end_the_game()

        self.fade_layout.update(self.world_shift)
        self.input()

        self.goal_collision()

        self.explosion_sprite.draw(self.display_surface)
        self.explosion_sprite.update(self.world_shift)


