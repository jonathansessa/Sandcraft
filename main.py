# To Do List
#  - Add liquid water
#  - Water needs to pool rather than stack
#  - Way to toggle between sand/water
#  - Add frame (so not screen edge)
#  - Add a shelf/solid element that works like edges

import pygame, sys, random
from pygame.locals import *

# Globals ----------------------------------------------------------------------------------------- #
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
FPS = 30

grains = []
dirty_rects = []

def main():
    global FPSCLOCK, DISPLAYSURF, font
    pygame.init()
    font = pygame.font.SysFont("Arial", 18)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

    mouse_x = 0
    mouse_y = 0
    generate_sand = False
    dirty_screen = False

    pygame.display.set_caption('Sandcraft')

    # Game Loop ------------------------------------------------------------------------------------ #
    while True:
        dirty_rects.clear()

        DISPLAYSURF.fill((0, 0, 0), pygame.Rect(0, 0, 30, 30))
        DISPLAYSURF.blit(update_fps(), (10, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                dirty_screen = True
                mouse_x, mouse_y = event.pos
                generate_sand = True
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                generate_sand = False

        if generate_sand:
            add_sand(mouse_x, mouse_y)

        update_sand()

        if len(dirty_rects) == 1 and dirty_screen:
            refresh_screen()
            dirty_screen = False

        pygame.display.update(dirty_rects)
        FPSCLOCK.tick(FPS)


def add_sand(x, y):
    grains.append([x, y])
    pix_obj = pygame.PixelArray(DISPLAYSURF)
    pix_obj[x][y] = (255, 255, 0)
    pix_obj.close()
    dirty_rects.append(pygame.Rect(x, y, 1, 1))


def update_sand():
    pix_obj = pygame.PixelArray(DISPLAYSURF)

    for grain in grains:
        if grain[1] < WINDOW_HEIGHT-1:
            if DISPLAYSURF.get_at((grain[0], grain[1]+1)) == (0, 0, 0):
                dirty_rects.append(pygame.Rect(grain[0], grain[1], 1, 2))
                pix_obj[grain[0], grain[1]] = (0, 0, 0)
                grain[1] += 1
                pix_obj[grain[0], grain[1]] = (255, 255, 0)
            elif DISPLAYSURF.get_at((grain[0], grain[1]+1)) == (255, 255, 0):
                if DISPLAYSURF.get_at((grain[0]-1, grain[1] + 1)) == (0, 0, 0):
                    dirty_rects.append(pygame.Rect(grain[0], grain[1], 1, 1))
                    dirty_rects.append(pygame.Rect(grain[0]-1, grain[1]+1, 1, 1))
                    pix_obj[grain[0], grain[1]] = (0, 0, 0)
                    grain[0] -= 1
                    grain[1] += 1
                    pix_obj[grain[0], grain[1]] = (255, 255, 0)
                elif DISPLAYSURF.get_at((grain[0]+1, grain[1] + 1)) == (0, 0, 0):
                    dirty_rects.append(pygame.Rect(grain[0], grain[1], 1, 1))
                    dirty_rects.append(pygame.Rect(grain[0]+1, grain[1]+1, 1, 1))
                    pix_obj[grain[0], grain[1]] = (0, 0, 0)
                    grain[0] += 1
                    grain[1] += 1
                    pix_obj[grain[0], grain[1]] = (255, 255, 0)
                else:
                    grains.remove(grain)
            else:
                grains.remove(grain)
        else:
            grains.remove(grain)

    pix_obj.close()


# Called when no animations are occurring to make sure no bugs
def refresh_screen():
    for y in range(1, WINDOW_HEIGHT-1):
        for x in range(1, WINDOW_WIDTH-1):
            if DISPLAYSURF.get_at([x, y]) == (255, 255, 0):
                if DISPLAYSURF.get_at([x-1, y+1]) == (0, 0, 0) or DISPLAYSURF.get_at([x, y+1]) == (0, 0, 0) or \
                        DISPLAYSURF.get_at([x+1, y+1]) == (0, 0, 0):
                    grains.append([x, y])


def update_fps():
    fps = str(int(FPSCLOCK.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color(0, 0, 255))
    dirty_rects.append(pygame.Rect(0, 0, 30, 30))
    return fps_text


if __name__ == '__main__':
    main()
