import pygame
import sys
import screen
from config import *
from driver import Driver
from screen import *


if __name__ == '__main__':
    pygame.init()

    screen_elements = screen.init_screen()
    display = screen_elements[0]
    element_menu = screen_elements[1]

    clock = pygame.time.Clock()

    driver = Driver()
    sandbox = pygame.Rect(MARGIN, MARGIN*2, SANDBOX_WIDTH, SANDBOX_HEIGHT)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                driver.update_on_key_down(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if element_menu.contains(event.pos[0], event.pos[1]):
                    element_menu.update(driver, event.pos[0], event.pos[1])

        driver.update_on_tick(pygame.mouse)

        # Blackout entire sandbox
        pygame.draw.rect(display, SANDBOX_COLOR, sandbox)

        driver.render(display)
        screen.update_fps(display, clock)
        pygame.display.flip()

        clock.tick(FPS)
