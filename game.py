import sys
import math
import random
import os

import pygame

from codefiles.classes.entities.entities import Player, Enemy
from codefiles.scripts.tilemap import Tilemap
from codefiles.classes.decor.clouds import Clouds
from codefiles.classes.decor.particles import Particle
from codefiles.classes.decor.spark import Spark
from codefiles.classes.entities.projectile import Projectile
from codefiles.scripts.dust import Dust
from codefiles.classes.decor.pieces import Piece
from codefiles.classes.interactive_objects.jump_pad import JumpPad
from codefiles.classes.interactive_objects.lever import Lever
from codefiles.classes.interactive_objects.door import Door
from codefiles.loading_scripts.loadAssets import getImages, getSounds
from codefiles.classes.gravity.gravity import Gravity
from codefiles.loading_scripts.load_level_variables import (
    load_levels_data,
    generate_level_variables,
)

SCREEN_WIDTH = 640 * 2
SCREEN_HEIGHT = 480 * 2
DISPLAY_WIDTH = 320
DISPLAY_HEIGHT = 240

GRAVITY_ENEMY = 0.1

TRANSPARENT_BLUE = (0, 0, 255, 50)
WHITE = (255, 255, 255)

levels_data = load_levels_data("levels.json")
(
    LEVELS,
    REVERSE_GRAVITY_LEVELS,
    TIMED_SWITCH_LEVELS,
    RESET_SWITCH_LEVELS,
    HEAVY_LEVELS,
    RANDOM_GRAVITY_LEVELS,
    SWITCH_ON_JUMP,
    STICKY_LEVELS,
    DIAL_LEVELS,
) = generate_level_variables(levels_data)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Gravity Rush")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT), pygame.SRCALPHA)
        self.display_2 = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.clock = pygame.time.Clock()

        self.frame = 0
        self.movement = [False, False]
        self.gravity_enemy = [0, GRAVITY_ENEMY]
        self.sound_factor = 0.5
        self.assets = getImages()
        self.sfx = getSounds(self.sound_factor)

        self.gun = False
        self.all_projectiles = []
        self.pieces = []

        self.gravity = Gravity()
        self.player = Player(self, (50, 50), (8, 15))
        self.tilemap = Tilemap(self, tile_size=16)

        self.level = 0
        self.load_level(LEVELS[self.level])
        self.screenshake = 0

    def displayLevel(self):
        level_display = pygame.Surface((100, 20), pygame.SRCALPHA)
        pygame.draw.rect(level_display, TRANSPARENT_BLUE, level_display.get_rect())

        font = pygame.font.Font(None, 16)
        level_text = font.render(LEVELS[self.level], True, WHITE)
        text_rect = level_text.get_rect(center=level_display.get_rect().center)
        level_display.blit(level_text, text_rect)

        self.display.blit(level_display, (100, 0))

    def setBackground(self):
        self.night = random.randint(0, 1)
        if self.night:
            self.clouds = Clouds(self.assets["stars"], count=100, moving=0)
        else:
            self.clouds = Clouds(self.assets["clouds"], count=16, moving=1)

    def createBlocks(self):
        self.ground_tile_positions = []
        for loc in self.tilemap.tilemap:
            tile = self.tilemap.tilemap[loc]
            if tile["type"] in {"grass", "stone", "wall", "block"}:
                self.ground_tile_positions.append(
                    (
                        tile["pos"][0] * self.tilemap.tile_size,
                        tile["pos"][1] * self.tilemap.tile_size,
                    )
                )

    def createDecor(self):
        self.leaf_spawners = []
        for tree in self.tilemap.extract([("large_decor", 2)], keep=True):
            self.leaf_spawners.append(
                pygame.Rect(4 + tree["pos"][0], 4 + tree["pos"][1], 23, 13)
            )

    def createObjects(self):
        self.jump_pads = []
        for jump_pad in self.tilemap.extract([("jump_pad", 0), ("jump_pad", 1)]):
            self.jump_pads.append(
                JumpPad(self, jump_pad["pos"], self.assets["jump_pad_anim"])
            )

        self.levers = []

        lever_variants = {
            0: ("lever90deg1", 0),
            1: ("lever180deg1", 0),
            2: ("lever270deg1", 0),
            3: ("lever0deg2", 1),
            4: ("lever180deg2", 1),
            5: ("lever270deg2", 1),
            6: ("lever0deg3", 2),
            7: ("lever90deg3", 2),
            8: ("lever270deg3", 2),
            9: ("lever0deg4", 3),
            10: ("lever90deg4", 3),
            11: ("lever180deg4", 3),
        }
        for lever in self.tilemap.extract(
            [
                ("lever", 0),
                ("lever", 1),
                ("lever", 2),
                ("lever", 3),
                ("lever", 4),
                ("lever", 5),
                ("lever", 6),
                ("lever", 7),
                ("lever", 8),
                ("lever", 9),
                ("lever", 10),
                ("lever", 11),
            ]
        ):
            variant = lever["variant"]
            asset_name, rotation = lever_variants[variant]
            self.levers.append(
                Lever(
                    lever["pos"],
                    self.assets[asset_name],
                    rotation,
                    self.gravity.switch_reset,
                )
            )

        self.doors = []
        for door in self.tilemap.extract([("door", 0), ("door", 1)]):
            if door["variant"] == 0:
                self.doors.append(Door(self, door["pos"], self.assets["door0"]))
            elif door["variant"] == 1:
                self.doors.append(Door(self, door["pos"], self.assets["door180"]))

    def createUnits(self):
        self.enemies = []
        for spawner in self.tilemap.extract(
            [("spawners", 0), ("spawners", 1), ("spawners", 2), ("spawners", 3)]
        ):
            if spawner["variant"] == 0:
                self.player.pos = spawner["pos"]
                self.player.air_time = 0
                self.player.velocity[0] = 0
                self.player.velocity[1] = 0
            elif spawner["variant"] == 1:
                self.enemies.append(Enemy(self, spawner["pos"], (8, 15), 0, 1, "enemy"))
            elif spawner["variant"] == 2:
                self.enemies.append(
                    Enemy(self, spawner["pos"], (24, 45), 1, 5, "enemy")
                )
            elif spawner["variant"] == 3:
                self.enemies.append(
                    Enemy(self, spawner["pos"], (100, 100), 0, 5, "dragon")
                )

    def placeGun(self):
        self.gun_pos = self.player.pos
        for _ in range(1000):
            x, y = random.choice(self.ground_tile_positions)
            y -= self.tilemap.tile_size
            if (
                not self.tilemap.solid_check((x, y))
                and abs(self.player.pos[0] - x) < 200
                and abs(self.player.pos[1] - y) < 50
            ):
                self.gun_pos = (x, y)
                break
        self.gun_size = (5, 5)
        self.gun_image = self.assets["gun"]
        self.gun_rect = self.gun_image.get_rect(center=self.gun_pos)

    def createDust(self, map_id):
        self.dusts = []
        if map_id in ["Insane-1", "Insane-2"]:
            for i in range(8):
                self.dusts.append(
                    Dust(self.assets["dust"], random.randint(-500, -470), i * 100 - 200)
                )
                self.dusts.append(
                    Dust(self.assets["dust"], random.randint(-400, -370), i * 100 - 200)
                )

    def load_level(self, map_id):
        self.frame = 0
        self.end = False
        self.gravity.loadGravityParameters(self.level)

        self.tilemap.load("data/maps/" + str(map_id) + ".json")
        self.createBlocks()
        self.setBackground()
        self.createDecor()
        self.createObjects()
        self.createUnits()
        self.placeGun()
        self.createDust(map_id)

        self.projectiles = []
        self.particles = []
        self.sparks = []

        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30

        self.lowest_block_position = self.tilemap.find_lowest_block_position()
        self.highest_block_position = self.tilemap.find_highest_block_position()
        self.leftest_block_position = self.tilemap.find_leftest_block_position()
        self.rightest_block_position = self.tilemap.find_rightest_block_position()

    def handle_projectiles(self, render_scroll):
        for projectile in self.projectiles.copy():
            projectile.collided = False
            projectile.update(self.player)
            projectile.render(self.display, render_scroll)

            if self.tilemap.wall_check(projectile.pos, projectile.speed):
                self.sfx["wall"].play()
                projectile.collided = True
                for _ in range(len(self.assets["pieces"])):
                    pos = [
                        projectile.pos[0] + random.random() * 20 - 10,
                        projectile.pos[1] + random.random() * 20 - 10,
                    ]
                    speed = [random.random() * 2 - 1, random.random()]
                    self.pieces.append(Piece(self.assets["pieces"][0], pos, speed))

            if self.tilemap.solid_check(projectile.pos):
                if projectile.weaponType == 1 or projectile.weaponType == 4:
                    projectile.collided = True

                elif projectile.weaponType == 2:
                    projectile.speed[1] = -projectile.speed[1] * 0.8
                    projectile.bounces += 1
                    if projectile.bounces == 5:
                        projectile.collided = True

                elif projectile.weaponType == 3:
                    projectile.collided = True
                    speed = [1, self.gravity.gravity[1] * 10]
                    spawn_velocities = [
                        [-speed[0], 0],
                        [speed[0], 0],
                        [0.5 * speed[0], 0],
                        [-0.5 * speed[0], 0],
                    ]
                    for velocity in spawn_velocities:
                        new_projectile = Projectile(
                            pos=[
                                projectile.pos[0] - projectile.speed[0],
                                projectile.pos[1] - projectile.speed[1],
                            ],
                            img=projectile.img,
                            speed=velocity,
                            entity=projectile.entity,
                            weaponType=2,
                            gravity=self.gravity.gravity,
                        )
                        self.projectiles.append(new_projectile)

                if projectile.collided:
                    for i in range(4):
                        self.sparks.append(
                            Spark(
                                projectile.pos,
                                random.random()
                                - 0.5
                                + (math.pi if projectile.speed[0] > 0 else 0),
                                2 + random.random(),
                            )
                        )

            elif projectile.time > projectile.maxTime:
                projectile.collided = True

            elif projectile.entity == 0:
                if (
                    self.player.rect().collidepoint(projectile.pos)
                    and abs(self.player.dashing) < 50
                ):
                    projectile.collided = True
                    self.dead += 1
                    self.sfx["hit"].play()
                    self.screenshake = max(16, self.screenshake)
                    self.create_particles(self.player)

            elif projectile.entity == 1:
                for enemy in self.enemies.copy():
                    if enemy.rect().collidepoint(projectile.pos):
                        projectile.collided = True
                        self.sfx["hit"].play()
                        if (
                            enemy.spawn != 1 and enemy.type != "dragon"
                        ) or enemy.headRect().collidepoint(projectile.pos):
                            enemy.health -= 1
                            self.create_particles(enemy)
                        if enemy.health <= 0:
                            self.enemies.remove(enemy)

            if projectile.collided:
                self.projectiles.remove(projectile)

    def create_particles(self, entity):
        self.sfx["hit"].play()
        for _ in range(30):
            angle = random.random() * math.pi * 2
            speed = random.random() * 5
            self.sparks.append(
                Spark(
                    entity.rect().center,
                    angle,
                    2 + random.random(),
                )
            )
            self.particles.append(
                Particle(
                    self,
                    "particle",
                    entity.rect().center,
                    velocity=[
                        math.cos(angle + math.pi) * speed * 0.5,
                        math.sin(angle + math.pi) * speed * 0.5,
                    ],
                    frame=random.randint(0, 7),
                )
            )

    def handle_particles(self, render_scroll):
        for rect in self.leaf_spawners:
            if random.random() * 49999 < rect.width * rect.height:
                pos = (
                    rect.x + random.random() * rect.width,
                    rect.y + random.random() * rect.height,
                )
                self.particles.append(
                    Particle(
                        self,
                        "leaf",
                        pos,
                        velocity=[-0.1, 0.3],
                        frame=random.randint(0, 20),
                    )
                )

        for particle in self.particles.copy():
            kill = particle.update()
            particle.render(self.display, offset=render_scroll)
            if particle.type == "leaf":
                particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
            if kill:
                self.particles.remove(particle)

        for spark in self.sparks.copy():
            kill = spark.update()
            spark.render(self.display, offset=render_scroll)
            if kill:
                self.sparks.remove(spark)

        for piece in self.pieces.copy():
            piece.update()
            piece.render(self.display, offset=render_scroll)
            if piece.pos[1] > self.player.pos[1] + 1000:
                self.pieces.remove(piece)

    def drawGun(self, render_scroll):
        if self.gun:
            gun_image = self.assets["gun"]
            gun_image = pygame.transform.scale(
                gun_image, (gun_image.get_width() * 2, gun_image.get_height() * 2)
            )
            gun_rect = gun_image.get_rect()
            square_size = max(gun_rect.width, gun_rect.height)
            square_surface = pygame.Surface(
                (square_size + 5, square_size + 5), pygame.SRCALPHA
            )
            square_surface1 = square_surface.copy()
            square_surface2 = square_surface.copy()
            square_surface3 = square_surface.copy()
            if self.player.weaponType == 1:
                square_surface1.fill((0, 0, 0, 100))
                square_surface2.fill((0, 0, 0, 255))
                square_surface3.fill((0, 0, 0, 255))
            elif self.player.weaponType == 2:
                square_surface1.fill((0, 0, 0, 255))
                square_surface2.fill((0, 0, 0, 100))
                square_surface3.fill((0, 0, 0, 255))
            elif self.player.weaponType == 3:
                square_surface1.fill((0, 0, 0, 255))
                square_surface2.fill((0, 0, 0, 255))
                square_surface3.fill((0, 0, 0, 100))

            square_rect1 = square_surface1.get_rect(topleft=(10, 10))
            square_rect2 = square_surface2.get_rect(topleft=(30, 10))
            square_rect3 = square_surface3.get_rect(topleft=(50, 10))

            gun_rect.topleft = [12, 15]
            gun_img = gun_image.copy()
            self.display.blit(square_surface1, square_rect1)
            self.display.blit(gun_img, gun_rect)

            gun_img = gun_image.copy()
            gun_img.fill(
                (
                    0,
                    255,
                    0,
                ),
                special_flags=pygame.BLEND_RGB_MULT,
            )
            gun_rect.topleft = [32, 15]
            self.display.blit(square_surface2, square_rect2)
            self.display.blit(gun_img, gun_rect)

            gun_img = gun_image.copy()
            gun_img.fill(
                (
                    255,
                    0,
                    0,
                ),
                special_flags=pygame.BLEND_RGB_MULT,
            )
            gun_rect.topleft = [52, 15]
            self.display.blit(square_surface3, square_rect3)
            self.display.blit(gun_img, gun_rect)

        else:
            self.display.blit(
                self.assets["gun"],
                (
                    self.gun_pos[0] + self.tilemap.tile_size / 2 - render_scroll[0],
                    self.gun_pos[1] - render_scroll[1],
                ),
            )

    def handleObjects(self, render_scroll):
        for enemy in self.enemies.copy():
            kill = enemy.update(self.tilemap, (0, 0), self.gravity_enemy)
            enemy.render(self.display, offset=render_scroll)
            if kill:
                self.enemies.remove(enemy)

        for jump_pad in self.jump_pads:
            if jump_pad.update(self.player.rect()):
                self.player.jump(
                    -50 * min(abs(self.player.gravity[0] + self.player.gravity[1]), 0.2)
                )
                self.sfx["jump_pad"].play()
            jump_pad.render(self.display, render_scroll)

        for lever in self.levers:
            if lever.update(self.player.rect()):
                self.gravity.gravity_direction = lever.direction
                self.gravity.switch_gravity = True
                if self.gravity.timed_switch and self.gravity.gravity_timer == 0:
                    self.gravity.gravity_timer = self.gravity.gravity_timer_max
                    self.gravity.gravity_temp = self.gravity.gravity
            lever.render(self.display, render_scroll)

        for door in self.doors:
            door.render(self.display, render_scroll)

    def handleUserInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = True
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = True
                if event.key == pygame.K_UP:
                    if self.player.jump():
                        self.sfx["jump"].play()
                if event.key == pygame.K_z and self.gun:
                    self.player.shoot()
                if event.key == pygame.K_c and self.gun:
                    self.player.weaponType += 1
                    if self.player.weaponType > 3:
                        self.player.weaponType = 1
                if event.key == pygame.K_s:
                    self.gravity.gravity_direction = 0
                    self.gravity.switch_gravity = True
                if event.key == pygame.K_a:
                    self.gravity.gravity_direction = 1
                    self.gravity.switch_gravity = True
                if event.key == pygame.K_w:
                    self.gravity.gravity_direction = 2
                    self.gravity.switch_gravity = True
                if event.key == pygame.K_d:
                    self.gravity.gravity_direction = 3
                    self.gravity.switch_gravity = True

                if event.key == pygame.K_e:
                    self.end = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = False
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = False

    def checkLevelEnd(self):
        for door in self.doors:
            if door.update(self.player.rect()):
                self.end = True

        if self.end == True:
            self.transition += 1
            if self.transition > 30:
                self.level = min(self.level + 1, len(os.listdir("data/maps")) - 1)
                self.load_level(LEVELS[self.level])
        if self.transition < 0:
            self.transition += 1

        if self.dead:
            self.dead += 1
            if self.dead == 10:
                self.transition = min(30, self.transition + 1)
            if self.dead > 40:
                self.load_level(LEVELS[self.level])
                self.gun = False

        for dust in self.dusts:
            if self.player.rect().colliderect(
                dust.x,
                dust.y,
                dust.image.get_width(),
                dust.image.get_height(),
            ):
                self.dead += 1

    def run(self):
        pygame.mixer.music.load("data/music.wav")
        pygame.mixer.music.set_volume(0.5 * self.sound_factor)
        pygame.mixer.music.play(-1)
        self.sfx["ambience"].play(-1)
        while True:
            self.checkLevelEnd()
            player = self.gravity.setGravity(self.frame, self.player, self)
            self.player = player
            self.frame += 1

            self.display.fill((0, 0, 0, 0))
            self.display_2.fill((19, 24, 98, 1))
            self.screenshake = max(0, self.screenshake - 1)

            for enemy in self.enemies:
                if enemy.spawn == 1 and random.random() < 0.001:
                    self.enemies.append(Enemy(self, enemy.pos, (8, 15), 0, 1, "enemy"))

            self.scroll[0] += (
                self.player.rect().centerx
                - self.display.get_width() / 2
                - self.scroll[0]
            ) / 30
            self.scroll[1] += (
                self.player.rect().centery
                - self.display.get_height() / 2
                - self.scroll[1]
            ) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            if not self.night:
                self.display_2.blit(self.assets["background"], (0, 0))

            self.clouds.update()
            self.clouds.render(self.display_2, offset=render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)
            self.tilemap.block_check(self.player)

            if self.gravity.sticky:
                if self.gravity.gravity[0] > 0 or self.gravity.gravity[1] < 0:
                    self.move = self.movement[0] - self.movement[1]
                else:
                    self.move = self.movement[1] - self.movement[0]
            else:
                if self.gravity.gravity[0] > 0:
                    self.move = self.movement[0] - self.movement[1]
                else:
                    self.move = self.movement[1] - self.movement[0]

            if not self.dead:
                if self.gravity.gravity[0] == 0:
                    self.player.update(
                        self.tilemap,
                        (self.move, 0),
                        self.gravity.gravity,
                    )
                elif self.gravity.gravity[1] == 0:
                    self.player.update(
                        self.tilemap,
                        (0, self.move),
                        self.gravity.gravity,
                    )

                self.player.render(self.display, offset=render_scroll)

            self.handleObjects(render_scroll)
            self.handle_projectiles(render_scroll)
            self.handle_particles(render_scroll)
            self.drawGun(render_scroll)

            for dust in self.dusts:
                dust.update(self.frame, self.player)
                dust.render(self.display, offset=render_scroll)

            list(map(lambda dust: dust.update(self.frame, self.player), self.dusts))
            list(
                map(
                    lambda dust: dust.render(self.display, offset=render_scroll),
                    self.dusts,
                )
            )

            display_mask = pygame.mask.from_surface(self.display)
            display_silhouette = display_mask.to_surface(
                setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0)
            )
            for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                self.display_2.blit(display_silhouette, offset)

            self.displayLevel()
            self.gravity.displayGravity(self.display)
            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(
                    transition_surf,
                    (255, 255, 255),
                    (self.display.get_width() // 2, self.display.get_height() // 2),
                    (30 - abs(self.transition)) * 8,
                )
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))

            self.display_2.blit(self.display, (0, 0))

            screenshake_offset = (
                random.random() * self.screenshake - self.screenshake / 2,
                random.random() * self.screenshake - self.screenshake / 2,
            )
            self.screen.blit(
                pygame.transform.smoothscale(self.display_2, self.screen.get_size()),
                screenshake_offset,
            )

            self.handleUserInput()
            pygame.display.update()
            self.clock.tick(60)
            # self.clock.tick(10)


Game().run()
