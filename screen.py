from config import *
from element_menu import *

PBAR_COLOR = (33, 33, 33)
TBAR_COLOR = (204, 204, 204)


def init_screen():
    pygame.display.set_caption('Sandcraft')
    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    tbar_height = math.floor(SANDBOX_HEIGHT * 0.3)
    tbar_width = (SANDBOX_WIDTH / 2) - (MARGIN / 2)

    pbar_height, pbar_width = tbar_height, tbar_width

    pbar_top = 3 * MARGIN + SANDBOX_HEIGHT
    tbar_top = pbar_top
    tbar_left = MARGIN
    pbar_left = 2 * MARGIN + tbar_width

    surface.fill(BG_COLOR)
    surface.fill(SANDBOX_COLOR, pygame.Rect(MARGIN, 2 * MARGIN, SANDBOX_WIDTH, SANDBOX_HEIGHT))
    surface.fill(TBAR_COLOR, pygame.Rect(tbar_left, tbar_top, tbar_width, tbar_height))

    surface.fill(PBAR_COLOR, pygame.Rect(pbar_left, pbar_top, pbar_width, pbar_height))

    # Top Menu Bar
    title_font = pygame.font.Font("fonts/RetroGaming.ttf", 22)
    title_text = title_font.render("SANDCRAFT", True, pygame.Color(255, 255, 255))
    surface.blit(title_text, (MARGIN, (2*MARGIN - 22)/3))

    # Particles Selection
    element_menu = ElementMenu(surface, pbar_left, pbar_top, pbar_width)

    return [surface, element_menu]


def in_sandbox(x, y):
    if x < MARGIN or MARGIN + SANDBOX_WIDTH < x:
        return False
    if y < MARGIN * 2 or MARGIN * 2 + SANDBOX_HEIGHT < y:
        return False
    return True


def update_fps(display, clock):
    fps = int(clock.get_fps())
    font = pygame.font.Font("./fonts/RetroGaming.ttf", 11)
    text = font.render(f"FPS: {fps}", True, (255, 255, 255), BG_COLOR)
    text_width = text.get_rect().width
    display.blit(text, (WINDOW_WIDTH - MARGIN - text_width, MARGIN))