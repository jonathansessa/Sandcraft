import sys
import pygame
from pygame.locals import *

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

DEF_COLOR = (0, 0, 0)
SAND_COLOR = (255, 255, 0)
WATER_COLOR = (0, 191, 255)
ROCK_COLOR = (211, 211, 211)


def update_sand(grains, surf):
    for grain in grains:
        if grain[1] < WINDOW_HEIGHT - 1 and 0 < grain[0] < WINDOW_WIDTH - 1:
            if surf.get_at((grain[0], grain[1]+1)) == DEF_COLOR:
                surf.set_at(grain, DEF_COLOR)
                grain[1] += 1
                surf.set_at(grain, SAND_COLOR)
            elif surf.get_at((grain[0]-1, grain[1]+1)) == DEF_COLOR:
                surf.set_at(grain, DEF_COLOR)
                grain[0] -= 1
                grain[1] += 1
                surf.set_at(grain, SAND_COLOR)
            elif surf.get_at((grain[0]+1, grain[1]+1)) == DEF_COLOR:
                surf.set_at(grain, DEF_COLOR)
                grain[0] += 1
                grain[1] += 1
                surf.set_at(grain, SAND_COLOR)
        else:
            continue


def update_water(drops, surf):
    for drop in drops:
        if drop[1] < WINDOW_HEIGHT - 1 and 0 < drop[0] < WINDOW_WIDTH - 1:
            if surf.get_at((drop[0], drop[1]+1)) == DEF_COLOR:
                surf.set_at(drop, DEF_COLOR)
                drop[1] += 1
                surf.set_at(drop, WATER_COLOR)
            elif surf.get_at((drop[0]-1, drop[1]+1)) == DEF_COLOR:
                surf.set_at(drop, DEF_COLOR)
                drop[0] -= 1
                drop[1] += 1
                surf.set_at(drop, WATER_COLOR)
            elif surf.get_at((drop[0]+1, drop[1]+1)) == DEF_COLOR:
                surf.set_at(drop, DEF_COLOR)
                drop[0] += 1
                drop[1] += 1
                surf.set_at(drop, WATER_COLOR)
            elif surf.get_at((drop[0]-1, drop[1])) == DEF_COLOR:
                surf.set_at(drop, DEF_COLOR)
                drop[0] -= 1
                surf.set_at(drop, WATER_COLOR)
            elif surf.get_at((drop[0]+1, drop[1])) == DEF_COLOR:
                surf.set_at(drop, DEF_COLOR)
                drop[0] += 1
                surf.set_at(drop, WATER_COLOR)
        else:
            continue


def main():
    pygame.init()
    DISPLAYSURFACE = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('SandCraft')
    FPS = pygame.time.Clock()

    drawing = False
    x = 0
    y = 0

    sand = []
    water = []
    element = 1

    run = True
    while run:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                run = False
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                drawing = True
            elif event.type == MOUSEBUTTONUP:
                drawing = False
            elif event.type == MOUSEMOTION and drawing:
                x, y = event.pos
            elif event.type == KEYDOWN:
                if event.key == K_1 or event.key == K_KP1:
                    element = 1
                elif event.key == K_2 or event.key == K_KP2:
                    element = 2
                elif event.key == K_3 or event.key == K_KP3:
                    element = 3

        if drawing:
            if element == 1:
                sand.append([x, y])
            elif element == 2:
                water.append([x, y])
            elif element == 3:
                pygame.draw.circle(DISPLAYSURFACE, ROCK_COLOR, (x, y), 4)

        update_sand(sand, DISPLAYSURFACE)
        update_water(water, DISPLAYSURFACE)

        pygame.display.update()
        FPS.tick(60)


if __name__ == '__main__':
    main()
