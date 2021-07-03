import pygame
import screen
from particle_data import template_steam
from start_menu import *
from driver import Driver


def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Display the start menu and store play mode
    mode = display_start_menu()

    # Create and define screen regions
    (display, sandbox, element_menu, tool_menu) = screen.init_screen(mode)
    driver = Driver(mode, element_menu, display)

    if mode == "DISCOVERY":
        element_menu.discovery_demo()
        driver.undiscovered.append(template_steam)

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
                    if driver.get_tool() == "LINE" or driver.get_tool() == "RECT" or driver.get_tool() == "OVAL":
                        driver.start_shape(pygame.mouse.get_pos())
                elif element_menu.contains(event.pos[0], event.pos[1]):
                    element_menu.update(driver, event.pos[0], event.pos[1])
                elif tool_menu.contains(event.pos[0], event.pos[1]):
                    tool_menu.update(driver, event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                driver.set_tool_use(False)
                driver.end_active_shape()
                if sandbox.collidepoint(pygame.mouse.get_pos()):
                    if driver.get_tool() == "LINE":
                        driver.end_line(pygame.mouse.get_pos())
                    elif driver.get_tool() == "RECT":
                        driver.end_rect(pygame.mouse.get_pos())
                    elif driver.get_tool() == "OVAL":
                        driver.end_oval(pygame.mouse.get_pos())

        # Update particle positions and apply tool (if is being used)
        driver.update_particles(pygame.mouse, sandbox, display)

        # Draw all particles in the sandbox
        driver.render(display)

        # Replace mouse pointer inside sandbox, otherwise show
        if sandbox.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_visible(False)
            driver.draw_tool_outline(pygame.mouse.get_pos(), sandbox, display)
        else:
            pygame.mouse.set_visible(True)

        # Update and show FPS (used for debugging)
        screen.update_fps(display, clock)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
