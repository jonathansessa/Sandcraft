import pygame
import math

SANDBOX_WIDTH = 800
SANDBOX_HEIGHT = 600

MARGIN = 14

SANDBOX_X = MARGIN
SANDBOX_Y = MARGIN * 2

WINDOW_WIDTH = SANDBOX_WIDTH + (MARGIN * 2)
WINDOW_HEIGHT = SANDBOX_HEIGHT + (MARGIN * 4) + math.floor(SANDBOX_HEIGHT * 0.3)

FPS = 60
PARTICLE_SIZE = 4

FONT_COLOR = (255, 255, 255)

BG_COLOR = (33, 33, 33)
SANDBOX_COLOR = (0, 0, 0)
