import pygame
import neat
import time
import os
import sys
import random

from Dino import *
from Obstacle import *
from Background import *

pygame.init()
pygame.font.init()

GEN = 0
HI = 0

WIN_WIDTH = 900
WIN_HEIGHT = 400
Background_LVL = 300

STAT_FONT = pygame.font.SysFont('comicsans', 25)


def draw_window(win, background, dinos, obstacles, score, hi, gen):
    win.fill((255, 255, 255))
    background.draw(win)

    text = STAT_FONT.render("Score: " + str(int(score/5)), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH-10-text.get_width(), 10))
    text = STAT_FONT.render("HI: " + str(int(hi/5)), 1, (0, 0, 0))
    win.blit(text, (WIN_WIDTH-10-text.get_width(), 30))

    gen = STAT_FONT.render("Gen: " + str(gen), 1, (0, 0, 0))
    win.blit(gen, (10, 10))
    for dino in dinos:
        dino.draw(win)
        # pygame.draw.rect(dino.img, (255, 0, 0), (0, 0, 50, 50), 2)
    for obstacle in obstacles:
        obstacle.draw(win)
        # pygame.draw.rect(obstacle.img, (255, 0, 0), (0, 0, obstacle.img.get_width(), obstacle.img.get_height()), 2)
    pygame.display.update()


def main(genomes, config):
    global GEN, HI
    GEN += 1

    nets = []
    ge = []
    dinos = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        dinos.append(Dino(100, Background_LVL+20))
        g.fitness = 0
        ge.append(g)

    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    background = Background(Background_LVL, WIN_HEIGHT // 5)
    obstacles = [Obstacle(WIN_WIDTH-300, Background_LVL+20)]
    obstacles.append(Obstacle(obstacles[-1].x, Background_LVL+20))

    background.initVel()
    obstacles[0].initVel()

    clock = pygame.time.Clock()
    score = 0
    run = True
    while run:
        clock.tick(90)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run == False
                pygame.display.quit()
                pygame.quit()
                quit()
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         dino.jump()

        obstacle_ind = 0
        if len(dinos) > 0:
            if len(obstacles) > 1 and dinos[0].x > obstacles[0].x + obstacles[0].img.get_width():
                obstacle_ind = 1
        else:
            run = False
            break

        for x, dino in enumerate(dinos):
            dino.move()
            ge[x].fitness += 0.1
            output = nets[x].activate((
                                    dino.x+dino.img.get_width(),                                        \
                                    dino.y,                                                             \
                                    obstacles[obstacle_ind].x,                                          \
                                    obstacles[obstacle_ind].y+obstacles[obstacle_ind].img.get_height(), \
                                    obstacles[0].VEL,                                                   \
                                    abs(obstacles[obstacle_ind].x - obstacles[obstacle_ind+1].x)        \
                                    ))

            if output[0] > 0.80:
                dino.jump()
            # elif output[1] > 0.80:
            #     dino.duck()
            #     print("Ducked")
            # else:
            #     pass

        #     print(dino.yvel, end=" ")
        # print()

        rem = []
        add_obstacle = False
        for obstacle in obstacles:
            for x, dino in enumerate(dinos):
                if obstacle.collide(dino):
                    ge[x].fitness -= 1
                    dinos.pop(x)
                    nets.pop(x)
                    ge.pop(x)

                # if not obstacle.passed and obstacle.x < dino.x:
                #     obstacle.passed = True
                #     add_obstacle = True
            if not obstacle.passed and obstacle.x < WIN_WIDTH // 2:
                obstacle.passed = True
                add_obstacle = True

            if obstacle.x + obstacle.img.get_width() < 0:
                rem.append(obstacle)

            obstacle.move()
        
        # if pygame.time.get_ticks() % 10 == 0:
        score += 1
        if score > HI:
            HI = score

        if score % 500 == 0:
            obstacles[-1].updateVel(0.1)
            background.updateVel(0.1)

        if add_obstacle:
            for g in ge:
                g.fitness += 5
            obstacles.append(Obstacle(obstacles[-1].x, Background_LVL+20))
        for r in rem:
            obstacles.remove(r)

        background.move()
        dino.move()
        draw_window(win, background, dinos, obstacles, score, HI, GEN)


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)




'''

output = nets[x].activate((dino.x, abs(dino.x - obstacles[obstacle_ind].x), dino.y, abs(dino.y - (obstacles[obstacle_ind].y + obstacles[obstacle_ind].img.get_height()))))
output = nets[x].activate((dino.x, obstacles[obstacle_ind].x, dino.y, obstacles[obstacle_ind].y))

output = nets[x].activate((dino.x, obstacles[obstacle_ind].x, obstacles[obstacle_ind].img.get_width(), \
                           dino.y, obstacles[obstacle_ind].y, obstacles[obstacle_ind].img.get_height()))
'''