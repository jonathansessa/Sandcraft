import pygame, sys, random
from pygame.locals import *
from particle import *
from operator import itemgetter

# Globals ----------------------------------------------------------------------------------------- #
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
FPS = 30

sand = []
water = []
dirty_rects = []


def main():
    global FPSCLOCK, DISPLAYSURF, font
    pygame.init()
    font = pygame.font.SysFont("Arial", 18)
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)

    mouse_x = 0
    mouse_y = 0
    generate_particle = False
    selected_material = 1

    pygame.display.set_caption('Sandcraft')

    # Game Loop ------------------------------------------------------------------------------------ #
    while 1:
        dirty_rects.clear()

        # Show FPS
        DISPLAYSURF.fill((0, 0, 0), pygame.Rect(0, 0, 30, 30))
        DISPLAYSURF.blit(update_fps(), (10, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                generate_particle = True
            elif event.type == MOUSEBUTTONUP:
                mouse_x, mouse_y = event.pos
                generate_particle = False
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    selected_material = 1
                elif event.key == K_2:
                    selected_material = 2
                elif event.key == K_3:
                    selected_material = 3

        if generate_particle:
            if selected_material == 1:
                add_sand_square(mouse_x, mouse_y)
            elif selected_material == 2:
                add_water_square(mouse_x, mouse_y)
            elif selected_material == 3:
                add_wood_square(mouse_x, mouse_y)

        update_particles(sand)
        update_liquid(water)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def add_sand(x, y):
    sand.append([x, y])
    pix_obj = pygame.PixelArray(DISPLAYSURF)
    pix_obj[x][y] = COLOR_SAND
    pix_obj.close()
    dirty_rects.append(pygame.Rect(x, y, 1, 1))


def add_water(x, y):
    water.append([x, y])
    pix_obj = pygame.PixelArray(DISPLAYSURF)
    pix_obj[x][y] = COLOR_WATER
    pix_obj.close()
    dirty_rects.append(pygame.Rect(x, y, 1, 1))


def add_sand_square(x, y):
    for i in range(50):
        add_sand(random.randint(x-20, x+20), random.randint(y-20, y+20))


def add_water_square(x, y):
    for i in range(50):
        add_water(random.randint(x-20, x+20), random.randint(y-20, y+20))


def add_wood_square(x, y):
    pygame.draw.rect(DISPLAYSURF, COLOR_WOOD, (x-10, y-10, 20, 20))


# Does liquid need to keep updating unless (1) has all solid neighbors, (2) surrounded by liquid?
def update_liquid(drops):
    pix_obj = pygame.PixelArray(DISPLAYSURF)

    s_drops = sorted(drops, key=itemgetter(1), reverse=True)

    for d in s_drops:
        # If particle is at bottom on screen
        if d[1] == WINDOW_HEIGHT - 1:
            drops.remove(d)
        # If particle is empty
        elif DISPLAYSURF.get_at((d[0], d[1])) == COLOR_AIR:
            drops.remove(d)
        # If space below is empty
        elif DISPLAYSURF.get_at((d[0], d[1]+1)) == COLOR_AIR:
            swap_particles(d[0], d[1], d[0], d[1]+1, pix_obj)
            d[1] += 1
        # If bottom left space is empty
        elif d[0] > 0 and DISPLAYSURF.get_at((d[0] - 1, d[1] + 1)) == COLOR_AIR:
            swap_particles(d[0], d[1], d[0] - 1, d[1] + 1, pix_obj)
            d[0] -= 1
            d[1] += 1
        # If bottom right space is empty
        elif d[0] < WINDOW_WIDTH - 2 and DISPLAYSURF.get_at((d[0] + 1, d[1] + 1)) == COLOR_AIR:
            swap_particles(d[0], d[1], d[0] + 1, d[1] + 1, pix_obj)
            d[0] += 1
            d[1] += 1
        # If left is empty
        elif d[0] > 0 and DISPLAYSURF.get_at((d[0] - 1, d[1])) == COLOR_AIR:
            swap_particles(d[0], d[1], d[0] - 1, d[1], pix_obj)
            d[0] -= 1
        # If right is empty
        elif d[0] < WINDOW_WIDTH - 2 and DISPLAYSURF.get_at((d[0] + 1, d[1])) == COLOR_AIR:
            swap_particles(d[0], d[1], d[0] + 1, d[1], pix_obj)
            d[0] += 1

    pix_obj.close()


def swap_particles(x1, y1, x2, y2, pix_obj):
    c1 = DISPLAYSURF.get_at((x1, y1))
    c2 = DISPLAYSURF.get_at((x2, y2))
    pix_obj[x1, y1] = c2
    pix_obj[x2, y2] = c1


def update_particles(particles):
    pix_obj = pygame.PixelArray(DISPLAYSURF)

    # Sort list so particles are updated bottom to top
    s_particles = sorted(particles, key=itemgetter(1), reverse=True)

    for p in s_particles:
        # If particle is at bottom on screen
        if p[1] == WINDOW_HEIGHT-1:
            particles.remove(p)
        # If particle is empty
        elif DISPLAYSURF.get_at((p[0], p[1])) == COLOR_AIR:
            particles.remove(p)
        # If space below is empty
        elif DISPLAYSURF.get_at((p[0], p[1]+1)) == COLOR_AIR:
            swap_particles(p[0], p[1], p[0], p[1]+1, pix_obj)
            p[1] += 1
        # If particle below is solid
        elif is_solid(DISPLAYSURF.get_at((p[0], p[1]+1))):
            # If bottom left space is empty
            if p[0] > 0 and DISPLAYSURF.get_at((p[0]-1, p[1]+1)) == COLOR_AIR:
                swap_particles(p[0], p[1], p[0]-1, p[1]+1, pix_obj)
                p[0] -= 1
                p[1] += 1
            # If bottom right space is empty
            elif p[0] < WINDOW_WIDTH-2 and DISPLAYSURF.get_at((p[0]+1, p[1]+1)) == COLOR_AIR:
                swap_particles(p[0], p[1], p[0]+1, p[1]+1, pix_obj)
                p[0] += 1
                p[1] += 1
            else:
                particles.remove(p)
        # Particle doesn't move
        else:
            particles.remove(p)

    pix_obj.close()


def update_fps():
    fps = str(int(FPSCLOCK.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color(0, 0, 255))
    dirty_rects.append(pygame.Rect(0, 0, 30, 30))
    return fps_text


if __name__ == '__main__':
    main()
