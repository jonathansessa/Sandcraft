import pygame.mouse
from sandcraft import screen
from sandcraft.start_menu import *
from sandcraft.driver import Driver
from sandcraft.config import TOMENU_EVENT_TYPE
from sandcraft.music_mixer import MusicMixer


def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Display the start menu and store play mode
    music = MusicMixer()
    mode = display_start_menu()

    # Create and define screen regions
    (display, sandbox, element_menu, tool_menu) = screen.init_screen(mode)

    driver = Driver(mode, element_menu, display, music)

    if mode == "DISCOVERY":
        undiscovered = ["basalt", "steam", "fire", "water"]
        element_menu.discovery_init(undiscovered)
        driver.undiscovered.extend(undiscovered)

    while 1:
        # Blackout entire sandbox (should optimize in the future)
        pygame.draw.rect(display, SANDBOX_COLOR, sandbox)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == TOMENU_EVENT_TYPE:
                music.endMixer()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sandbox.collidepoint(pygame.mouse.get_pos()):
                    driver.set_tool_use(True)
                    if driver.get_tool() == "LINE" or driver.get_tool() == "RECT" or driver.get_tool() == "OVAL":
                        driver.start_shape(pygame.mouse.get_pos())
                elif element_menu.contains(event.pos[0], event.pos[1]):
                    element_menu.update(driver, event.pos[0], event.pos[1])
                elif tool_menu.contains(event.pos[0], event.pos[1]):
                    tool_menu.update(driver, event.pos[0], event.pos[1], True)
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
        driver.update_particles(pygame.mouse)

        # Draw all particles in the sandbox
        driver.render(display)

        # Replace mouse pointer inside sandbox, otherwise show
        if sandbox.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_visible(False)
            driver.draw_tool_outline(pygame.mouse.get_pos(), sandbox, display)
        else:
            pygame.mouse.set_visible(True)
            pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
            element_menu.draw_tooltip(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            if tool_menu.contains(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                tool_menu.update(driver, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], False)

        # Update and show FPS (used for debugging)
        screen.update_fps(display, clock)
        pygame.display.flip()
        clock.tick(FPS)


def loop_main():
    while 1:
        main()


if __name__ == '__main__':
    loop_main()
