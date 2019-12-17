import pygame
import os
import random

OBSTACLE_IMG = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "tree-sm-1.png")), (30, 40)),
                pygame.transform.scale(pygame.image.load(os.path.join("imgs", "tree-sm-2.png")), (50, 40)),
                pygame.transform.scale(pygame.image.load(os.path.join("imgs", "tree-md-1.png")), (40, 47)),
                pygame.transform.scale(pygame.image.load(os.path.join("imgs", "tree-lg-3.png")), (70, 55)),
                pygame.transform.scale(pygame.image.load(os.path.join("imgs", "tree-lg-4.png")), (90, 60))]


class Obstacle:

    def __init__(self, prev_x, y):
        self.x = prev_x + random.randint(300, 700)
        self.y = y
        self.img = OBSTACLE_IMG[random.randint(0, len(OBSTACLE_IMG)-1)]
        self.passed = False
    
    def move(self):
        self.x -= self.VEL
    
    def draw(self, win):
        win.blit(self.img, (self.x, self.y - self.img.get_rect().height))
    
    def collide(self, dino):
        dino_mask = dino.get_mask()
        obstacle_mask = pygame.mask.from_surface(self.img)

        obstacle_offset = (int(self.x) - dino.x + dino.img.get_rect().width, self.y - round(dino.y))

        x_point = dino_mask.overlap(obstacle_mask, obstacle_offset)

        if x_point:
            return True

        return False

    def initVel(self):
        Obstacle.VEL = 4

    def updateVel(self, dv):
        Obstacle.VEL *= (1+dv)
