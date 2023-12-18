import pygame


class Door:
    def __init__(self, game, pos, img):
        self.game = game
        self.pos = pos
        self.animation = img.copy()
        self.active = False

    def update(self, player_rect):
        if player_rect.colliderect(pygame.Rect(self.pos[0], self.pos[1], 16, 16)):
            self.active = True
            return True

        if self.animation.done:
            self.active = False

        if self.active:
            self.animation.update()

    def render(self, surf, offset=(0, 0)):
        image = self.animation.img()
        surf.blit(image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
