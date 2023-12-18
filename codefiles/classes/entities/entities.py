import math
import random

import pygame

from ..decor.particles import Particle
from ..decor.spark import Spark
from .projectile import Projectile


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.newPos = self.pos
        self.shiftPos = 0
        self.size = size
        self.dashing = 0
        self.velocity = [0, 0]
        self.movement = [0, 0]
        self.collisions = {"up": False, "down": False, "right": False, "left": False}
        self.action = ""
        self.anim_offset = (-3, -3)
        self.flip = False if self.type != "dragon" else True
        self.set_action("idle")

        if self.type == "dragon":
            self.pos[1] -= 25
        self.gravity = self.game.gravity.gravity

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def rectFromSide(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[1], self.size[0])

    def newRect(self):
        return pygame.Rect(self.newPos[0], self.newPos[1], self.size[0], self.size[1])

    def newRectFromSide(self):
        return pygame.Rect(self.newPos[0], self.newPos[1], self.size[1], self.size[0])

    def headRect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1] / 3)

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.type + "/" + self.action].copy()
            self.animation.frame = 0

    def newPosition(self, tilemap):
        self.pos[0] += self.velocity[0]
        if self.gravity[0] == 0:
            entity_rect = self.rect()
        elif self.gravity[1] == 0:
            entity_rect = self.rectFromSide()

        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.velocity[0] > 0:
                    self.pos[0] -= self.velocity[0]
                    self.collisions["right"] = True
                if self.velocity[0] < 0:
                    self.pos[0] -= self.velocity[0]
                    self.collisions["left"] = True

        self.pos[1] += self.velocity[1]
        if self.gravity[0] == 0:
            entity_rect = self.rect()
        elif self.gravity[1] == 0:
            entity_rect = self.rectFromSide()

        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if self.velocity[1] > 0:
                    self.pos[1] -= self.velocity[1]
                    self.collisions["down"] = True
                if self.velocity[1] < 0:
                    self.pos[1] -= self.velocity[1]
                    self.collisions["up"] = True

        if self.collisions["down"] or self.collisions["up"]:
            self.velocity[1] = 0
        if self.collisions["left"] or self.collisions["right"]:
            self.velocity[0] = 0

    def getVelocity(self, movement):
        if self.gravity[0] == 0:
            maxX = 1.5
            maxY = 5
            frictionX = 0.10
            frictionY = 0
        elif self.gravity[1] == 0:
            maxX = 5
            maxY = 1.5
            frictionX = 0
            frictionY = 0.10

        if self.type == 'player':
            factor = 0.15
        else:
            factor = 0.22
        
        self.velocity[1] = self.velocity[1] + self.gravity[1] + movement[1] * factor
        self.velocity[0] = self.velocity[0] + self.gravity[0] + movement[0] * factor

        if self.velocity[1] > 0:
            self.velocity[1] = min(max(self.velocity[1] - frictionY, 0), maxY)
        elif self.velocity[1] < 0:
            self.velocity[1] = max(min(self.velocity[1] + frictionY, 0), -maxY)

        if self.velocity[0] > 0:
            self.velocity[0] = min(max(self.velocity[0] - frictionX, 0), maxX)
        elif self.velocity[0] < 0:
            self.velocity[0] = max(min(self.velocity[0] + frictionX, 0), -maxX)

    def getDirection(self, movement):
        if self.type == 'player':
            if self.gravity[0] == 0:
                if movement[0] > 0:
                    self.flip = False
                if movement[0] < 0:
                    self.flip = True
            elif self.gravity[1] == 0:
                if movement[1] > 0:
                    self.flip = False
                if movement[1] < 0:
                    self.flip = True

    def update(self, tilemap, movement=(0, 0)):
        self.collisions = {"up": False, "down": False, "right": False, "left": False}

        self.getVelocity(movement)
        self.newPosition(tilemap)
        
        self.getDirection(movement)
        self.animation.update()

    def draw_health_bar(self, surf, offset=(0, 0)):
        bar_width = self.size[0]
        bar_height = 5
        bar_x = self.pos[0] - offset[0]
        bar_y = self.pos[1] - offset[1] - bar_height - 5

        health_percentage = max(self.health / self.maxHealth, 0.0)
        pygame.draw.rect(surf, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(
            surf,
            (0, 255, 0),
            (bar_x, bar_y, int(bar_width * health_percentage), bar_height),
        )

    def render(self, surf, offset=(0, 0), spawn=0):
        if abs(self.dashing) <= 50:
            if self.gravity[0] > 0:
                img = pygame.transform.rotate(self.animation.img(), 90)
                img = pygame.transform.flip(img, False, abs(self.flip - 1))
            elif self.gravity[0] < 0:
                img = pygame.transform.rotate(self.animation.img(), -90)
                img = pygame.transform.flip(img, False, self.flip)
            elif self.gravity[1] < 0:
                img = pygame.transform.rotate(self.animation.img(), 180)
                img = pygame.transform.flip(img, abs(self.flip - 1), False)
            elif self.gravity[1] > 0:
                img = self.animation.img()
                img = pygame.transform.flip(img, self.flip, False)

            if spawn == 1 or self.type == "dragon":
                img = pygame.transform.scale(img, self.size)

            surf.blit(
                img,
                (
                    self.pos[0] - offset[0] + self.anim_offset[0],
                    self.pos[1] - offset[1] + self.anim_offset[1],
                ),
            )

            if self.gun:
                gun_img = self.game.assets["gun"].copy()
                if self.weaponType == 2:
                    gun_img.fill((0, 255, 0), special_flags=pygame.BLEND_RGB_MULT)
                elif self.weaponType == 3:
                    gun_img.fill((255, 0, 0), special_flags=pygame.BLEND_RGB_MULT)

                if self.flip:
                    surf.blit(
                        pygame.transform.flip(gun_img, True, False),
                        (
                            self.rect().centerx
                            - 4
                            - self.game.assets["gun"].get_width()
                            - offset[0],
                            self.rect().centery - offset[1],
                        ),
                    )
                else:
                    surf.blit(
                        gun_img,
                        (
                            self.rect().centerx + 4 - offset[0],
                            self.rect().centery - offset[1],
                        ),
                    )
            if self.spawn == 1:
                self.draw_health_bar(surf, offset)


class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size, spawn, health, e_type):
        super().__init__(game, e_type, pos, size)
        self.spawn = spawn
        self.health = health
        self.maxHealth = health
        self.walking = 0
        self.idle = 1
        self.gun = True
        self.weaponType = 1

    def determineAction(self, movement):
        if movement[0] != 0:
            self.set_action("run")
        else:
            self.set_action("idle")

    def handleHit(self):
        if abs(self.game.player.dashing) >= 50:
            if self.rect().colliderect(self.game.player.rect()):
                self.game.screenshake = max(16, self.game.screenshake)
                self.game.sfx["hit"].play()
                for i in range(30):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 5
                    self.game.sparks.append(
                        Spark(self.rect().center, angle, 2 + random.random())
                    )
                    self.game.particles.append(
                        Particle(
                            self.game,
                            "particle",
                            self.rect().center,
                            velocity=[
                                math.cos(angle + math.pi) * speed * 0.5,
                                math.sin(angle + math.pi) * speed * 0.5,
                            ],
                            frame=random.randint(0, 7),
                        )
                    )
                self.game.sparks.append(
                    Spark(self.rect().center, 0, 5 + random.random())
                )
                self.game.sparks.append(
                    Spark(self.rect().center, math.pi, 5 + random.random())
                )
                self.health -= 1

    def shoot(self):
        self.game.sfx["shoot"].play()
        xSpeed = -2 if self.flip else 2
        self.game.projectiles.append(
            Projectile(
                [self.rect().centerx - 7, self.rect().centery],
                self.game.assets["projectile"],
                [xSpeed, 0],
                0,
                self.weaponType,
                self.gravity,
            )
        )
        for _ in range(4):
            self.game.sparks.append(
                Spark(
                    self.game.projectiles[-1].pos,
                    random.random() - 0.5 + math.pi * self.flip,
                    2 + random.random(),
                )
            )

    def update(self, tilemap, movement=(0, 0), gravity=[0, 0.1]):
        self.gravity = gravity
        if self.walking:
            if tilemap.solid_check(
                (
                    self.rect().centerx + (-7 if self.flip else 7),
                    self.pos[1] + self.size[1] + 1,
                )
            ):
                if self.collisions["right"] or self.collisions["left"]:
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])
            else:
                self.flip = not self.flip

            self.walking = max(0, self.walking - 1)
            if not self.walking:
                dis = (
                    self.game.player.pos[0] - self.pos[0],
                    self.game.player.pos[1] - self.pos[1],
                )
                if abs(dis[1]) < 16:
                    if (self.flip and dis[0] < 0) or (not self.flip and dis[0] > 0):
                        self.shoot()

        elif random.random() < 0.01:
            self.walking = random.randint(30, 120)

        super().update(tilemap, movement=movement)
        self.determineAction(movement)
        self.handleHit()
        return self.health <= 0


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        self.bounce = False
        self.cannon = True
        self.weaponType = 1
        self.spawn = 0
        self.gun = game.gun

    def getWeapon(self):
        if not self.game.gun and self.rect().colliderect(self.game.gun_rect):
            self.game.gun = True
            self.gun = True

        if self.game.gun:
            if self.weaponType == 1:
                pass
            elif self.weaponType == 2:
                self.bounce = True
            elif self.weaponType == 3:
                self.cannon = True

    def determineAction(self, movement):
        if self.air_time > 4:
            self.set_action("jump")
        elif movement[0] != 0 and self.gravity[0] == 0:
            self.set_action("run")
        elif movement[1] != 0 and self.gravity[1] == 0:
            self.set_action("run")
        else:
            self.set_action("idle")

    def handleJumps(self):
        if self.collisions["down"] and self.gravity[1] > 0:
            self.air_time = 0
            self.jumps = 1
        elif self.collisions["up"] and self.gravity[1] < 0:
            self.air_time = 0
            self.jumps = 1
        elif self.collisions["left"] and self.gravity[0] < 0:
            self.air_time = 0
            self.jumps = 1
        elif self.collisions["right"] and self.gravity[0] > 0:
            self.air_time = 0
            self.jumps = 1

    def jump(self, jump_power=-3):
        if self.jumps:
            if self.gravity[1] > 0:
                self.velocity[1] = jump_power
            elif self.gravity[1] < 0:
                self.velocity[1] = -jump_power
            elif self.gravity[0] < 0:
                self.velocity[0] = -jump_power
            elif self.gravity[0] > 0:
                self.velocity[0] = jump_power

            if self.game.gravity.switch_on_jump:
                self.game.gravity.switch_gravity = True
                self.game.gravity.gravity_direction = (
                    self.game.gravity_direction + 2
                ) % 4

            self.jumps -= 1
            self.air_time = 5
            return True

    def shoot(self):
        self.game.sfx["shoot"].play()

        if self.gravity[0] == 0:
            xSpeed = -2 if self.flip else 2
            ySpeed = 0
        else:
            xSpeed = 0
            ySpeed = -2 if self.flip else 2

        self.game.projectiles.append(
            Projectile(
                [self.rect().centerx, self.rect().centery],
                self.game.assets["projectile"],
                [xSpeed, ySpeed],
                1,
                self.weaponType,
                self.gravity,
            )
        )
        for _ in range(4):
            self.game.sparks.append(
                Spark(
                    self.game.projectiles[-1].pos,
                    random.random() - 0.5 + math.pi * self.flip,
                    2 + random.random(),
                )
            )

    def update(self, tilemap, movement=(0, 0), gravity=[0.1, 0]):
        self.gravity = gravity
        super().update(tilemap, movement=movement)

        self.getWeapon()
        self.air_time += 1

        if (
            self.pos[1] > (self.game.lowest_block_position[1] + 5) * 16
            or self.pos[1] < (self.game.highest_block_position[1] - 5) * 16
            or self.pos[0] > (self.game.rightest_block_position[0] + 5) * 16
            or self.pos[0] < (self.game.leftest_block_position[0] - 5) * 16
        ):
            if not self.game.dead:
                self.game.screenshake = max(16, self.game.screenshake)
            self.game.dead += 1

        self.handleJumps()
        self.determineAction(movement)
