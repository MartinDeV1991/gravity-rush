import pygame
from ..scripts.utils import load_image, load_images, Animation


def getImages():
    assets = {
        "decor": load_images("tiles/decor"),
        "grass": load_images("tiles/grass"),
        "wall": load_images("tiles/wall"),
        "block": load_images("tiles/block"),
        "large_decor": load_images("tiles/large_decor"),
        "stone": load_images("tiles/stone"),
        "player": load_image("entities/player.png"),
        "background": load_image("background.png"),
        "stars": load_image("star.png", 1),
        "clouds": load_images("clouds"),
        "enemy/idle": Animation(load_images("entities/enemy/idle"), img_dur=6),
        "enemy/run": Animation(load_images("entities/enemy/run"), img_dur=4),
        "enemy1/idle": Animation(load_images("entities/enemy1/idle"), img_dur=6),
        "enemy1/run": Animation(load_images("entities/enemy1/run"), img_dur=4),
        "dragon/idle": Animation(load_images("entities/dragon/idle", 1), img_dur=10),
        "dragon/run": Animation(load_images("entities/dragon/run", 1), img_dur=10),
        "dragon/attack": Animation(
            load_images("entities/dragon/attack", 1), img_dur=10, loop=False
        ),
        "player/idle": Animation(load_images("entities/player/idle"), img_dur=6),
        "player/run": Animation(load_images("entities/player/run"), img_dur=4),
        "player/jump": Animation(load_images("entities/player/jump")),
        "player/slide": Animation(load_images("entities/player/slide")),
        "player/wall_slide": Animation(load_images("entities/player/wall_slide")),
        "particle/leaf": Animation(
            load_images("particles/leaf"), img_dur=20, loop=False
        ),
        "particle/particle": Animation(
            load_images("particles/particle"), img_dur=6, loop=False
        ),
        "gun": load_image("gun.png"),
        "projectile": load_image("projectile.png"),
        "projectile2": load_image("projectile5.png", 1),
        "dust": load_image("dust1.png", 1),
        "pieces": load_images("broken_wall"),
        "jump_pad_anim": Animation(load_images("jump_pad"), img_dur=5, loop=False),
        "lever0deg1": Animation(load_images("lever/0deg1", 1), img_dur=10, loop=False),
        "lever90deg1": Animation(
            load_images("lever/90deg1", 1), img_dur=10, loop=False
        ),
        "lever180deg1": Animation(
            load_images("lever/180deg1", 1), img_dur=10, loop=False
        ),
        "lever270deg1": Animation(
            load_images("lever/270deg1", 1), img_dur=10, loop=False
        ),
        "lever0deg2": Animation(load_images("lever/0deg2", 1), img_dur=20, loop=False),
        "lever90deg2": Animation(
            load_images("lever/90deg2", 1), img_dur=10, loop=False
        ),
        "lever180deg2": Animation(
            load_images("lever/180deg2", 1), img_dur=10, loop=False
        ),
        "lever270deg2": Animation(
            load_images("lever/270deg2", 1), img_dur=10, loop=False
        ),
        "lever0deg3": Animation(load_images("lever/0deg3", 1), img_dur=10, loop=False),
        "lever90deg3": Animation(
            load_images("lever/90deg3", 1), img_dur=10, loop=False
        ),
        "lever180deg3": Animation(
            load_images("lever/180deg3", 1), img_dur=10, loop=False
        ),
        "lever270deg3": Animation(
            load_images("lever/270deg3", 1), img_dur=10, loop=False
        ),
        "lever0deg4": Animation(load_images("lever/0deg4", 1), img_dur=10, loop=False),
        "lever90deg4": Animation(
            load_images("lever/90deg4", 1), img_dur=10, loop=False
        ),
        "lever180deg4": Animation(
            load_images("lever/180deg4", 1), img_dur=10, loop=False
        ),
        "lever270deg4": Animation(
            load_images("lever/270deg4", 1), img_dur=10, loop=False
        ),
        "door0": Animation(load_images("door/0deg", 1), img_dur=10, loop=False),
        "door180": Animation(load_images("door/180deg", 1), img_dur=10, loop=False),
    }
    assets = scaleImages(assets)
    return assets


def scaleImages(assets):
    for i in range(len(assets["jump_pad_anim"].images)):
        assets["jump_pad_anim"].images[i] = pygame.transform.scale(
            assets["jump_pad_anim"].images[i], [16, 16]
        )

    for i in range(len(assets["lever0deg1"].images)):
        assets["lever0deg1"].images[i] = pygame.transform.scale(
            assets["lever0deg1"].images[i], [16, 16]
        )
    for i in range(len(assets["lever90deg1"].images)):
        assets["lever90deg1"].images[i] = pygame.transform.scale(
            assets["lever90deg1"].images[i], [16, 16]
        )
    for i in range(len(assets["lever180deg1"].images)):
        assets["lever180deg1"].images[i] = pygame.transform.scale(
            assets["lever180deg1"].images[i], [16, 16]
        )
    for i in range(len(assets["lever270deg1"].images)):
        assets["lever270deg1"].images[i] = pygame.transform.scale(
            assets["lever270deg1"].images[i], [16, 16]
        )

    for i in range(len(assets["lever0deg2"].images)):
        assets["lever0deg2"].images[i] = pygame.transform.scale(
            assets["lever0deg2"].images[i], [16, 16]
        )
    for i in range(len(assets["lever90deg2"].images)):
        assets["lever90deg2"].images[i] = pygame.transform.scale(
            assets["lever90deg2"].images[i], [16, 16]
        )
    for i in range(len(assets["lever180deg2"].images)):
        assets["lever180deg2"].images[i] = pygame.transform.scale(
            assets["lever180deg2"].images[i], [16, 16]
        )
    for i in range(len(assets["lever270deg2"].images)):
        assets["lever270deg2"].images[i] = pygame.transform.scale(
            assets["lever270deg2"].images[i], [16, 16]
        )

    for i in range(len(assets["lever0deg3"].images)):
        assets["lever0deg3"].images[i] = pygame.transform.scale(
            assets["lever0deg3"].images[i], [16, 16]
        )
    for i in range(len(assets["lever90deg3"].images)):
        assets["lever90deg3"].images[i] = pygame.transform.scale(
            assets["lever90deg3"].images[i], [16, 16]
        )
    for i in range(len(assets["lever180deg3"].images)):
        assets["lever180deg3"].images[i] = pygame.transform.scale(
            assets["lever180deg3"].images[i], [16, 16]
        )
    for i in range(len(assets["lever270deg3"].images)):
        assets["lever270deg3"].images[i] = pygame.transform.scale(
            assets["lever270deg3"].images[i], [16, 16]
        )

    for i in range(len(assets["lever0deg4"].images)):
        assets["lever0deg4"].images[i] = pygame.transform.scale(
            assets["lever0deg4"].images[i], [16, 16]
        )
    for i in range(len(assets["lever90deg4"].images)):
        assets["lever90deg4"].images[i] = pygame.transform.scale(
            assets["lever90deg4"].images[i], [16, 16]
        )
    for i in range(len(assets["lever180deg4"].images)):
        assets["lever180deg4"].images[i] = pygame.transform.scale(
            assets["lever180deg4"].images[i], [16, 16]
        )
    for i in range(len(assets["lever270deg4"].images)):
        assets["lever270deg4"].images[i] = pygame.transform.scale(
            assets["lever270deg4"].images[i], [16, 16]
        )

    for i in range(len(assets["door0"].images)):
        assets["door0"].images[i] = pygame.transform.scale(
            assets["door0"].images[i], [16, 16]
        )

    for i in range(len(assets["door180"].images)):
        assets["door180"].images[i] = pygame.transform.scale(
            assets["door180"].images[i], [16, 16]
        )
    return assets


def getSounds(sound_factor):
    sfx = {
        "jump": pygame.mixer.Sound("data/sfx/jump.wav"),
        "dash": pygame.mixer.Sound("data/sfx/dash.wav"),
        "hit": pygame.mixer.Sound("data/sfx/hit.wav"),
        "shoot": pygame.mixer.Sound("data/sfx/shoot.wav"),
        "ambience": pygame.mixer.Sound("data/sfx/ambience.wav"),
        "wall": pygame.mixer.Sound("data/sfx/break5.wav"),
        "jump_pad": pygame.mixer.Sound("data/sfx/jump_pad.mp3"),
    }

    sfx["jump"].set_volume(0.7 * sound_factor)
    sfx["dash"].set_volume(0.3 * sound_factor)
    sfx["hit"].set_volume(0.8 * sound_factor)
    sfx["shoot"].set_volume(0.4 * sound_factor)
    sfx["ambience"].set_volume(0.2 * sound_factor)
    sfx["wall"].set_volume(0.4 * sound_factor)
    sfx["jump_pad"].set_volume(0.7 * sound_factor)

    return sfx
