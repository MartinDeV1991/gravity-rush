import pygame


class Lever:
    def __init__(self, pos, img, direction, reset):
        self.pos = pos
        self.animation = img.copy()
        self.active = False
        self.pulled = False
        self.direction = direction
        self.reset = reset

    def update(self, player_rect):
        if (
            player_rect.colliderect(pygame.Rect(self.pos[0], self.pos[1], 16, 16))
            and self.pulled == False
        ):
            self.active = True
            self.animation.done = False
            self.pulled = True
            return True

        if self.animation.done:
            self.active = False
            if self.reset:
                self.pulled = False
            self.animation.done = False

        if self.active:
            self.animation.update()

    def render(self, surf, offset=(0, 0)):
        image = self.animation.img()
        surf.blit(image, (self.pos[0] - offset[0], self.pos[1] - offset[1]))
