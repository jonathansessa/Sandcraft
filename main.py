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

        update_solid(sand)
        update_liquid(water)

        print(len(sand), ", ", len(water))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def add_sand(x, y):
    sand.append(Particle(x, y, pygame.time.get_ticks()))
    pix_obj = pygame.PixelArray(DISPLAYSURF)
    pix_obj[x][y] = COLOR_SAND
    pix_obj.close()


def add_water(x, y):
    water.append(Particle(x, y, pygame.time.get_ticks()))
    pix_obj = pygame.PixelArray(DISPLAYSURF)
    pix_obj[x][y] = COLOR_WATER
    pix_obj.close()


# Adds fifty random sand pixels to sand[], sorts from bottom->top, left->right
def add_sand_square(x, y):
    for i in range(50):
        add_sand(random.randint(x-20, x+20), random.randint(y-20, y+20))


def add_water_square(x, y):
    for i in range(50):
        add_water(random.randint(x-20, x+20), random.randint(y-20, y+20))


def add_wood_square(x, y):
    pygame.draw.rect(DISPLAYSURF, COLOR_WOOD, (x-10, y-10, 20, 20))


def swap_pixels(x1, y1, x2, y2, pix_obj):
    c1 = DISPLAYSURF.get_at((x1, y1))
    c2 = DISPLAYSURF.get_at((x2, y2))
    pix_obj[x1, y1] = c2
    pix_obj[x2, y2] = c1


def update_liquid(drops):
    drops.sort(key=lambda s: (s.y, s.x), reverse=True)
    pix_obj = pygame.PixelArray(DISPLAYSURF)

    for d in drops:
        # If particle is empty/not a liquid
        if not is_liquid(DISPLAYSURF.get_at((d.x, d.y))):
            drops.remove(d)

        # If particle is at bottom on screen
        elif d.y == WINDOW_HEIGHT - 1:
            drops.remove(d)

        # If pixel below particle is empty
        elif DISPLAYSURF.get_at((d.x, d.y + 1)) == COLOR_AIR:
            # Update drops's downward velocity
            d.update_vy(1)
            dest = d.y + d.vy

            # Calculate new y-value
            new_y = check_y_path(d.x, d.y, dest)
            swap_pixels(d.x, d.y, d.x, new_y, pix_obj)
            d.y = new_y
            d.t = pygame.time.get_ticks()

            # If hit an obstacle
            if new_y != dest:
                d.vy = 0

        # Obstacle immediately below particle
        else:
            if is_liquid(DISPLAYSURF.get_at((d.x, d.y+1))):
                # If bottom left space is empty
                if d.x > 0 and DISPLAYSURF.get_at((d.x-1, d.y + 1)) == COLOR_AIR:
                    swap_pixels(d.x, d.y, d.x-1, d.y+1, pix_obj)
                    d.x -= 1
                    d.y += 1
                    d.update_vx(-1)
                    d.t = pygame.time.get_ticks()
                # If bottom right space is empty
                elif d.x < WINDOW_WIDTH-2 and DISPLAYSURF.get_at((d.x+1, d.y + 1)) == COLOR_AIR:
                    swap_pixels(d.x, d.y, d.x+1, d.y+1, pix_obj)
                    d.x += 1
                    d.y += 1
                    d.update_vx(1)
                    d.t = pygame.time.get_ticks()
                # If left space is empty
                elif d.x > 0 and DISPLAYSURF.get_at((d.x - 1, d.y)) == COLOR_AIR:
                    # Update drop's leftward velocity
                    d.update_vx(-1)
                    dest = d.x + d.vx

                    # Calculate new x-value
                    new_x = check_x_path(d.x, d.y, dest)
                    swap_pixels(d.x, d.y, new_x, d.y, pix_obj)
                    d.x = new_x
                    d.t = pygame.time.get_ticks()

                    # If hit an obstacle
                    if new_x != dest:
                        d.vx = 0
                # If right space is empty
                elif d.x < WINDOW_WIDTH-2 and DISPLAYSURF.get_at((d.x+1, d.y)) == COLOR_AIR:
                    # Update drop's rightward velocity
                    d.update_vx(1)
                    dest = d.x + d.vx

                    # Calculate new x-value
                    new_x = check_x_path(d.x, d.y, dest)
                    swap_pixels(d.x, d.y, new_x, d.y, pix_obj)
                    d.x = new_x
                    d.t = pygame.time.get_ticks()

                    # If hit an obstacle
                    if new_x != dest:
                        d.vx = 0

    pix_obj.close()


def update_solid(particles):
    particles.sort(key=lambda s: (s.y, s.x), reverse=True)
    pix_obj = pygame.PixelArray(DISPLAYSURF)

    for p in particles:
        # If particle is empty/not a solid
        if not is_solid(DISPLAYSURF.get_at((p.x, p.y))):
            particles.remove(p)

        # If particle is at bottom on screen
        elif p.y == WINDOW_HEIGHT - 1:
            particles.remove(p)

        # If pixel below particle is empty
        elif DISPLAYSURF.get_at((p.x, p.y + 1)) == COLOR_AIR:
            # Update particle's downward velocity
            p.update_vy(1)
            dest = p.y + p.vy

            # Calculate new y-value
            new_y = check_y_path(p.x, p.y, dest)
            swap_pixels(p.x, p.y, p.x, new_y, pix_obj)
            p.y = new_y
            p.t = pygame.time.get_ticks()

            # If hit an obstacle
            if new_y != dest:
                p.vy = 0

        # Obstacle immediately below particle
        else:
            if not is_solid(DISPLAYSURF.get_at((p.x, p.y+1))):
                swap_pixels(p.x, p.y, p.x, p.y + 1, pix_obj)
                if is_liquid(DISPLAYSURF.get_at((p.x, p.y))):
                    water.append(Particle(p.x, p.y, pygame.time.get_ticks()))
                p.y += 1
                p.t = pygame.time.get_ticks()
                if is_liquid(DISPLAYSURF.get_at((p.x, p.y))):
                    water.append(Particle(p.x, p.y, pygame.time.get_ticks()))

            # If bottom left space is empty/liquid
            elif p.x > 0 and not is_solid(DISPLAYSURF.get_at((p.x-1, p.y+1))):
                swap_pixels(p.x, p.y, p.x-1, p.y+1, pix_obj)
                if is_liquid(DISPLAYSURF.get_at((p.x, p.y))):
                    water.append(Particle(p.x, p.y, pygame.time.get_ticks()))
                p.x -= 1
                p.y += 1
                p.t = pygame.time.get_ticks()
            # If bottom right space is empty/liquid
            elif p.x < WINDOW_WIDTH-2 and not is_solid(DISPLAYSURF.get_at((p.x+1, p.y+1))):
                swap_pixels(p.x, p.y, p.x+1, p.y+1, pix_obj)
                if is_liquid(DISPLAYSURF.get_at((p.x, p.y))):
                    water.append(Particle(p.x, p.y, pygame.time.get_ticks()))
                p.x += 1
                p.y += 1
                p.t = pygame.time.get_ticks()
            # Particle doesn't move
            else:
                if pygame.time.get_ticks() - p.t > 1000:
                    particles.remove(p)

    pix_obj.close()


# Moves y value until reaches destination, or hits another particle
def check_x_path(x1, y1, destination):
    # Moving right
    if destination > x1:
        if destination > WINDOW_WIDTH - 1:
            destination = WINDOW_WIDTH - 1

        while x1 != destination:
            if DISPLAYSURF.get_at((x1 + 1, y1)) == COLOR_AIR:
                x1 += 1
            else:
                return x1
    # Moving left
    else:
        if destination < 0:
            destination = 0

        while x1 != destination:
            if DISPLAYSURF.get_at((x1 - 1, y1)) == COLOR_AIR:
                x1 -= 1
            else:
                return x1

    return x1


# Moves y value until reaches destination, or hits another particle
def check_y_path(x1, y1, destination):
    # Moving down
    if destination > y1:
        if destination > WINDOW_HEIGHT-1:
            destination = WINDOW_HEIGHT-1

        while y1 != destination:
            if DISPLAYSURF.get_at((x1, y1+1)) == COLOR_AIR:
                y1 += 1
            else:
                return y1
    # Moving down
    else:
        if destination < 0:
            destination = 0

        while y1 != destination:
            if DISPLAYSURF.get_at((x1, y1 - 1)) == COLOR_AIR:
                y1 -= 1
            else:
                return y1

    return y1


def update_fps():
    fps = str(int(FPSCLOCK.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color(0, 140, 255))
    return fps_text


if __name__ == '__main__':
    main()
