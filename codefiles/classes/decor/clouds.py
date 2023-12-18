import random
import pygame


class Cloud:
    def __init__(self, pos, size, img, speed, depth):
        self.pos = list(pos)
        self.img = img
        self.size = size
        self.speed = speed
        self.depth = depth

    def update(self):
        self.pos[0] += self.speed

    def render(self, surf, offset=(0, 0)):
        render_pos = (
            self.pos[0] - offset[0] * self.depth,
            self.pos[1] - offset[1] * self.depth,
        )

        if self.depth == 0:
            surf.blit(
                pygame.transform.smoothscale(self.img, (self.size, self.size)),
                (
                    render_pos[0] % (surf.get_width() + self.img.get_width())
                    - self.img.get_width(),
                    render_pos[1] % (surf.get_height() + self.img.get_height())
                    - self.img.get_height(),
                ),
            )
        else:
            surf.blit(
                self.img,
                (
                    render_pos[0] % (surf.get_width() + self.img.get_width())
                    - self.img.get_width(),
                    render_pos[1] % (surf.get_height() + self.img.get_height())
                    - self.img.get_height(),
                ),
            )


class Clouds:
    def __init__(self, cloud_images, count=16, moving=0):
        self.clouds = []

        for _ in range(count):
            if moving == 1:
                img = random.choice(cloud_images)
                speed = random.random() * 0.05 + 0.05
                depth = random.random() * 0.6 + 0.2
                size = 1
            else:
                img = cloud_images
                speed = 0
                depth = 0
                size = random.randint(0, 10)

            self.clouds.append(
                Cloud(
                    (random.random() * 99999, random.random() * 99999),
                    size,
                    img,
                    speed,
                    depth,
                )
            )

        self.clouds.sort(key=lambda x: x.depth)

    def update(self):
        for cloud in self.clouds:
            cloud.update()

    def render(self, surf, offset=(0, 0)):
        for cloud in self.clouds:
            cloud.render(surf, offset=offset)
