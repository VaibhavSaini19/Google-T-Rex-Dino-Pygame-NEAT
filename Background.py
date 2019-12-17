import pygame
import os

BASE_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "base.png")), (900, 30))
CLOUD_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "cloud.png")), (80, 30))

class Background:
    base_img = BASE_IMG
    BASE_WIDTH = BASE_IMG.get_width()

    cloud_img = CLOUD_IMG
    CLOUD_WIDTH = CLOUD_IMG.get_width()
    CLOUD_GAP = BASE_WIDTH // 3

    def __init__(self, base_y, cloud_y):
        self.base_y = base_y
        self.base_x1 = 0
        self.base_x2 = self.BASE_WIDTH
        self.cloud_y = cloud_y
        self.cloud_x1 = self.CLOUD_GAP
        self.cloud_x2 = 2 * self.cloud_x1
        self.cloud_x3 = 3 * self.cloud_x1

    def move(self):
        self.base_x1 -= self.BASE_VEL
        self.base_x2 -= self.BASE_VEL
        if self.base_x1 + self.BASE_WIDTH < 0:
            self.base_x1 = self.base_x2 + self.BASE_WIDTH
        if self.base_x2 + self.BASE_WIDTH < 0:
            self.base_x2 = self.base_x1 + self.BASE_WIDTH

        self.cloud_x1 -= self.CLOUD_VEL
        self.cloud_x2 -= self.CLOUD_VEL
        self.cloud_x3 -= self.CLOUD_VEL
        if self.cloud_x1 + self.CLOUD_WIDTH < 0:
            self.cloud_x1 = self.cloud_x3 + self.CLOUD_GAP
        if self.cloud_x2 + self.CLOUD_WIDTH < 0:
            self.cloud_x2 = self.cloud_x1 + self.CLOUD_GAP
        if self.cloud_x3 + self.CLOUD_WIDTH < 0:
            self.cloud_x3 = self.cloud_x2 + self.CLOUD_GAP

    def draw(self, win):
        win.blit(self.base_img, (self.base_x1, self.base_y))
        win.blit(self.base_img, (self.base_x2, self.base_y))

        win.blit(self.cloud_img, (self.cloud_x1, self.cloud_y - 2*self.cloud_img.get_height()))
        win.blit(self.cloud_img, (self.cloud_x2, self.cloud_y + 2*self.cloud_img.get_height()))
        win.blit(self.cloud_img, (self.cloud_x3, self.cloud_y))

    def initVel(self):
        Background.BASE_VEL = 4
        Background.CLOUD_VEL = 1

    def updateVel(self, dv):
        Background.BASE_VEL *= (1+dv)
        Background.CLOUD_VEL *= (1+dv)