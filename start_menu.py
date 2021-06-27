import pygame
import sys
from config import *


def create_menu_button(menu, text, y):
    button = pygame.Rect(0, 0, 400, 45)
    button.center = (MENU_WIDTH/2, y)
    pygame.draw.rect(menu, (180, 180, 180), button)
    pygame.draw.rect(menu, (255, 255, 255), button, 1)

    font = pygame.font.Font("fonts/RetroGaming.ttf", 36)
    label = font.render(text, False, (0, 0, 0))
    menu.blit(label, (button.x + ((button.width-label.get_width()) / 2), button.y))

    return button


def display_start_menu():
    clock = pygame.time.Clock()
    menu = pygame.display.set_mode((MENU_WIDTH, MENU_HEIGHT))

    menu.fill(BG_COLOR)

    title_font = pygame.font.Font('fonts/RetroGaming.ttf', 60)
    title = title_font.render("SANDCRAFT", False, (255, 255, 255))
    title_rect = title.get_rect()
    title_rect.center = (MENU_WIDTH/2, MENU_HEIGHT/3)
    menu.blit(title, title_rect)

    y = math.floor((1/2) * MENU_HEIGHT)
    sandbox_button = create_menu_button(menu, "SANDBOX MODE", y)
    discovery_button = create_menu_button(menu, "DISCOVERY MODE", y + 60)
    quit_button = create_menu_button(menu, "QUIT GAME", y + 120)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sandbox_button.collidepoint(pygame.mouse.get_pos()):
                    return "SANDBOX"
                elif discovery_button.collidepoint(pygame.mouse.get_pos()):
                    return "DISCOVERY"
                elif quit_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        clock.tick(15)