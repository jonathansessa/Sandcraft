import math
import pygame
from pygame.locals import *
from element_menu import *

BG_COLOR = (77, 77, 77)
SANDBOX_COLOR = (0, 0, 0)
PBAR_COLOR = (204, 204, 204)
TBAR_COLOR = (204, 204, 204)


def init_screen():
    sandbox_width = 800
    sandbox_height = 600

    margin = math.floor(sandbox_width * 0.02)

    tbar_height = math.floor(sandbox_height * 0.3)
    tbar_width = (sandbox_width / 2) - (margin / 2)

    pbar_height, pbar_width = tbar_height, tbar_width

    window_width = 2 * margin + sandbox_width
    window_height = 4 * margin + sandbox_height + tbar_height

    pbar_top = 3 * margin + sandbox_height
    tbar_top = pbar_top
    tbar_left = margin
    pbar_left = 2 * margin + tbar_width

    pygame.display.set_caption('Sandcraft')
    surface = pygame.display.set_mode((window_width, window_height))

    surface.fill(BG_COLOR)
    surface.fill(SANDBOX_COLOR, pygame.Rect(margin, 2 * margin, sandbox_width, sandbox_height))
    surface.fill(TBAR_COLOR, pygame.Rect(tbar_left, tbar_top, tbar_width, tbar_height))

    surface.fill(PBAR_COLOR, pygame.Rect(pbar_left, pbar_top, pbar_width, pbar_height))
    #pygame.draw.lines(surface, (255, 255, 255), False, [(pbar_left, pbar_top + pbar_height), (pbar_left, pbar_top), (pbar_left + pbar_width, pbar_top)])
    #pygame.draw.lines(surface, (0, 0, 0), False, [(pbar_left, pbar_top + pbar_height), (pbar_left + pbar_width, pbar_top + pbar_height), (pbar_left + pbar_width, pbar_top)])

    # Menu Bar
    font = pygame.font.SysFont("arial", 20)
    title_text = font.render("SANDCRAFT", True, pygame.Color(0, 0, 0))
    surface.blit(title_text, (margin, margin/2))

    # Particles
    p_menu = ElementMenu(surface, pbar_left, pbar_top, pbar_width)



