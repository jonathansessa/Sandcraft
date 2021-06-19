import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from driver import Driver


def load_fonts(size_list):
    font_dict = {}

    for size in size_list:
        font_dict[size] = pygame.font.SysFont("Times New Roman", size)

    return font_dict


def render_fps(display, clock, pos, font, color):
    text = font.render(str(int(clock.get_fps())), 0, color)
    display.blit(text, pos)


if __name__ == '__main__':
    pygame.init()

    display = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Sandcraft")

    clock = pygame.time.Clock()

    font_dict = load_fonts([8, 16, 32])

    driver = Driver()

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                driver.update_on_key_down(event)

        driver.update_on_tick(pygame.mouse)

        display.fill((0, 0, 0))
        driver.render(display)
        render_fps(
            display,
            clock,
            (0, 0),
            font_dict.get(32),
            (254, 254, 254))
        pygame.display.flip()

        clock.tick(FPS)
