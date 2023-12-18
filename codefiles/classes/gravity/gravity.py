import math
import random
import pygame

from ...loading_scripts.load_level_variables import (
    load_levels_data,
    generate_level_variables,
)
from ..entities.entities import PhysicsEntity, Player

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

GRAVITY_HIGH = 0.5
GRAVITY_LOW = 0.1


class Gravity:
    def __init__(self):
        self.gravity_reset = 0
        self.gravity_direction_old = 0
        self.gravity_timer = 0
        self.original_gravity = GRAVITY_LOW
        self.gravity = [0, self.original_gravity]
        self.gravity_temp = self.gravity
        self.gravity_timer_max = 500
        self.switch_gravity = False

    def loadGravityParameters(self, level):
        if LEVELS[level] in STICKY_LEVELS:
            self.sticky = True
        else:
            self.sticky = False

        if LEVELS[level] in DIAL_LEVELS:
            self.dial = True
        else:
            self.dial = False

        if LEVELS[level] in HEAVY_LEVELS:
            self.original_gravity = GRAVITY_HIGH
        else:
            self.original_gravity = GRAVITY_LOW

        if LEVELS[level] in RANDOM_GRAVITY_LEVELS:
            self.random_gravity = True
        else:
            self.random_gravity = False

        if LEVELS[level] in REVERSE_GRAVITY_LEVELS:
            self.gravity = [0, -self.original_gravity]
            self.gravity_direction = 2
        else:
            self.gravity = [0, self.original_gravity]
            self.gravity_direction = 0

        if LEVELS[level] in SWITCH_ON_JUMP:
            self.switch_on_jump = True
        else:
            self.switch_on_jump = False

        if LEVELS[level] in RESET_SWITCH_LEVELS:
            self.switch_reset = True
        else:
            self.switch_reset = False

        if LEVELS[level] in TIMED_SWITCH_LEVELS:
            self.timed_switch = True
        else:
            self.timed_switch = False

    def setGravity(self, frame, player, game):
        if self.gravity_reset > 0:
            self.gravity_reset -= 1

        if self.gravity[0] > 0:
            self.gravity_direction_old = 3
        elif self.gravity[0] < 0:
            self.gravity_direction_old = 1
        elif self.gravity[1] > 0:
            self.gravity_direction_old = 0
        elif self.gravity[1] < 0:
            self.gravity_direction_old = 2

        if not self.gravity_reset:
            if self.timed_switch:
                if self.gravity_timer > 0:
                    self.gravity_timer -= 1
                else:
                    # if self.gravity != self.gravity_temp:
                    # self.player.velocity[1] = 0
                    # self.player.velocity[0] = 0
                    self.gravity = self.gravity_temp

            if self.random_gravity:
                if random.random() > 0.99:
                    self.switch_gravity = True
                    self.gravity_direction = random.choice([0, 1, 2, 3])

            if self.sticky:
                if player.collisions["down"] == True:
                    self.switch_gravity = True
                    self.gravity_direction = 0
                elif player.collisions["up"] == True:
                    self.switch_gravity = True
                    self.gravity_direction = 2
                elif player.collisions["left"] == True:
                    self.switch_gravity = True
                    self.gravity_direction = 1
                elif player.collisions["right"] == True:
                    self.switch_gravity = True
                    self.gravity_direction = 3

        if self.dial:
            if self.gravity[0] == 0:
                self.gravity[1] = abs(math.sin(frame / 500) / 5)
                if self.gravity[1] == 0:
                    self.gravity[1] += 0.01
            elif self.gravity[1] == 0:
                self.gravity[0] = math.sin(frame / 500) / 5
                if self.gravity[0] == 0:
                    self.gravity[0] += 0.01

        if self.switch_gravity:
            self.gravity_reset = 5
            self.switch_gravity = False
            sizeDiff = player.size[1] - player.size[0]
            # print(sizeDiff)
            # print(player.size[0])
            # print(player.size[1])
            match self.gravity_direction:
                case 0:
                    self.gravity = [0, self.original_gravity]
                    # self.player.velocity[0] = 0
                    if (
                        self.gravity_direction_old == 1
                        or self.gravity_direction_old == 3
                    ):
                        if game.tilemap.solid_check(
                            [player.pos[0] + 7, player.pos[1] - player.size[0]]
                        ):
                            player.pos[1] += player.size[0]
                        elif game.tilemap.solid_check(
                            [player.pos[0] + 7, player.pos[1] + player.size[0]]
                        ):
                            player.pos[1] -= player.size[0]
                case 1:
                    self.gravity = [-self.original_gravity, 0]
                    # self.player.velocity[1] = 0
                    if (
                        self.gravity_direction_old == 0
                        or self.gravity_direction_old == 2
                    ):
                        if game.tilemap.solid_check(
                            [player.pos[0] - player.size[1], player.pos[1] + 7]
                        ):
                            player.pos[0] += player.size[1]
                        elif game.tilemap.solid_check(
                            [player.pos[0] + player.size[1], player.pos[1] + 7]
                        ):
                            player.pos[0] -= player.size[1]
                case 2:
                    self.gravity = [0, -self.original_gravity]
                    # self.player.velocity[0] = 0
                    if (
                        self.gravity_direction_old == 1
                        or self.gravity_direction_old == 3
                    ):
                        if game.tilemap.solid_check(
                            [player.pos[0] + 7, player.pos[1] - player.size[0]]
                        ):
                            player.pos[1] += player.size[0]
                        elif game.tilemap.solid_check(
                            [player.pos[0] + 7, player.pos[1] + player.size[0]]
                        ):
                            player.pos[1] -= player.size[0]
                case 3:
                    self.gravity = [self.original_gravity, 0]
                    # self.player.velocity[1] = 0
                    if (
                        self.gravity_direction_old == 0
                        or self.gravity_direction_old == 2
                    ):
                        if game.tilemap.solid_check(
                            [player.pos[0] - player.size[1], player.pos[1] + 7]
                        ):
                            player.pos[0] += player.size[1]
                        elif game.tilemap.solid_check(
                            [player.pos[0] + player.size[1], player.pos[1] + 7]
                        ):
                            player.pos[0] -= player.size[1]
        return player

    def displayGravity(self, surf):
        X = 50
        Y = 100
        size = 20
        if self.gravity[0] > 0:
            xpos = X - size
            ypos = Y
            xpos1 = X - abs(self.gravity[0] * 100)
            ypos1 = Y
            xsize = 20
            ysize = 10
        elif self.gravity[0] < 0:
            xpos = X
            ypos = Y
            xpos1 = X
            ypos1 = Y
            xsize = 20
            ysize = 10
        elif self.gravity[1] > 0:
            xpos = X
            ypos = Y
            xpos1 = X
            ypos1 = Y
            xsize = 10
            ysize = 20
        elif self.gravity[1] < 0:
            xpos = X
            ypos = Y - size
            xpos1 = X
            ypos1 = Y - abs(self.gravity[1] * 100)
            xsize = 10
            ysize = 20

        if self.gravity[0] == 0:
            gravity_display1 = pygame.Surface(
                (10, abs(self.gravity[1] * 100)), pygame.SRCALPHA
            )
        elif self.gravity[1] == 0:
            gravity_display1 = pygame.Surface(
                (abs(self.gravity[0] * 100), 10), pygame.SRCALPHA
            )

        gravity_display = pygame.Surface((xsize, ysize), pygame.SRCALPHA)

        color = (255, 0, 0)
        color1 = (0, 255, 0)

        pygame.draw.rect(gravity_display, color, gravity_display.get_rect())
        pygame.draw.rect(gravity_display1, color1, gravity_display1.get_rect())

        surf.blit(gravity_display, (xpos, ypos))
        surf.blit(gravity_display1, (xpos1, ypos1))
