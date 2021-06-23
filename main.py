import pygame
import sys
import screen
from config import *
from driver import Driver
from screen import *


if __name__ == '__main__':
    pygame.init()

    # Create and define screen regions
    screen_elements = screen.init_screen()
    display = screen_elements[0]
    sandbox = screen_elements[1]
    element_menu = screen_elements[2]
    tool_menu = screen_elements[3]

    clock = pygame.time.Clock()
    driver = Driver()

    while 1:
        # Blackout entire sandbox (should optimize in the future)
        pygame.draw.rect(display, SANDBOX_COLOR, sandbox)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sandbox.collidepoint(pygame.mouse.get_pos()):
                    driver.set_tool_use(True)
                elif element_menu.contains(event.pos[0], event.pos[1]):
                    element_menu.update(driver, event.pos[0], event.pos[1])
                elif tool_menu.contains(event.pos[0], event.pos[1]):
                    tool_menu.update(driver, event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                driver.set_tool_use(False)

        # Replace mouse pointer inside sandbox, otherwise show
        if sandbox.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_visible(False)
            driver.draw_tool_outline(pygame.mouse.get_pos(), sandbox, display)
        else:
            pygame.mouse.set_visible(True)

        # Update particle positions and apply tool (if is being used)
        driver.update_particles(pygame.mouse)

        # Draw all particles in the sandbox
        driver.render(display)

        # Update and show FPS (used for debugging)
        screen.update_fps(display, clock)
        pygame.display.flip()
        clock.tick(FPS)
