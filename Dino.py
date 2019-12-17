import pygame
import os

DINO_SIZE = 50
DINO_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "trex-still.png")), (DINO_SIZE, DINO_SIZE)),
             pygame.transform.scale(pygame.image.load(os.path.join("imgs", "trex-left.png")), (DINO_SIZE, DINO_SIZE)),
             pygame.transform.scale(pygame.image.load(os.path.join("imgs", "trex-right.png")), (DINO_SIZE, DINO_SIZE))]

class Dino:
    IMGS = DINO_IMGS
    JUMP_DIST = -6
    GRAVITY = 0.13
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.yvel = 0
        self.ground_pos = self.y
        self.tick_count = 0
        self.img = self.IMGS[0]
        

    def jump(self):
        if self.y == self.ground_pos:
            self.yvel = self.JUMP_DIST

    def duck(self):
        self.yvel = -self.JUMP_DIST

    def draw(self, win):
        win.blit(self.img, (self.x - DINO_SIZE, self.y - DINO_SIZE))

    def move(self):
        self.y += self.yvel
        self.yvel = round(self.yvel + self.GRAVITY, 2)
        self.y = constrain(self.y, 0, self.ground_pos)

        self.tick_count += 1
        if self.y == self.ground_pos:
            if self.tick_count % 20 < 10:
                self.img = self.IMGS[1]
            else:
                self.img = self.IMGS[2]
        else:
            self.img = self.IMGS[0]


    def get_mask(self):
        return pygame.mask.from_surface(self.img)


def constrain(n, minn, maxn):
    return max(min(maxn, n), minn)
