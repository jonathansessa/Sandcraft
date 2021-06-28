import pygame
from .config import FONT_PATH
from .particle_data import ELEMENTS


class ElementMenu:
    pygame.font.init()
    FONT = pygame.font.Font(FONT_PATH, 11)
    FONT_COLOR = (255, 255, 255)
    BUTTON_SIZE = 18
    MARGIN = 6

    def __init__(self, surface, x, y, width, mode):
        self._surface = surface
        self._x = x
        self._y = y
        self._width = width
        self._height = 300
        self._mode = mode
        self.element_buttons = []
        self.draw()

    # Creates the menu by building each section based on particle_data
    def draw(self):
        sect_x = self._x
        sect_y = self._y
        sect_w = self._width / 2 - self.MARGIN
        for category in ELEMENTS:
            sect_h = self.create_section(self._surface, sect_x, sect_y, sect_w, category, ELEMENTS[category])
            sect_x += sect_w + self.MARGIN
            if sect_x >= self._x + self._width:
                sect_x = self._x
                sect_y += sect_h + 2 * self.MARGIN

    # First checks if a button was clicked, then changes corresponding button to active
    def update(self, driver, x, y):
        for b in self.element_buttons:
            if b.contains(x, y):
                for button in self.element_buttons:
                    button.set_inactive()
                    if button.contains(x, y) and button.unlocked:
                        button.set_active()
                        driver.set_current_element(button.get_element())
                    button.update()

    def contains(self, x, y):
        if x < self._x or self._x + self._width < x:
            return False
        if y < self._y or self._y + self._height < y:
            return False
        return True

    def create_section(self, surface, x, y, width, title, elements):
        t = self.FONT.render(title, True, self.FONT_COLOR)
        surface.blit(t, (x, y))

        left = x
        top = y + t.get_height() + self.MARGIN/2

        for e in elements:
            self.element_buttons.append(self.ElementButton(surface, left, top, self.BUTTON_SIZE, self.BUTTON_SIZE, e, self._mode))
            left += self.BUTTON_SIZE + self.MARGIN
            if left + self.BUTTON_SIZE > x + width:
                left = x
                top += self.BUTTON_SIZE + self.MARGIN

        return top + self.BUTTON_SIZE - self._y

    def discovery_demo(self):
        for button in self.element_buttons:
            if button.get_element().name != "Steam":
                button.unlocked = True
                button.update()

    class ElementButton:
        ACTIVE_COLOR = (255, 0, 0)

        def __init__(self, surface, x, y, width, height, template_particle, mode):
            self._surface = surface
            self._x = x
            self._y = y
            self._width = width
            self._height = height
            self._particle = template_particle
            self._active = False
            self._enabled = True
            self._unlocked = (mode == "SANDBOX")
            self.update()

        # Redraws button based on particle and if unlocked/enabled/active
        def update(self):
            button = pygame.Rect(self._x, self._y, self._width, self._height)

            # If element is locked draw a black square with a question mark, otherwise draw square with element color
            if not self._unlocked:
                pygame.draw.rect(self._surface, (0, 0, 0), button)
                font = pygame.font.Font(FONT_PATH, 11)
                q_mark = font.render("?", True, pygame.Color(255, 255, 255))
                self._surface.blit(q_mark, (self._x + 4, self._y + 1))
            else:
                pygame.draw.rect(self._surface, self._particle.color, button)

            # If element is not enabled, draw a semi-transparent white square over it
            if not self._enabled:
                s = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
                s.fill((150, 150, 150, 180))
                self._surface.blit(s, (self._x, self._y))

            # If element is currently active/selected, draw a red line around button
            if self._active:
                pygame.draw.lines(self._surface, self.ACTIVE_COLOR, True, ((self._x, self._y),
                                                                         (self._x + self._width-1, self._y),
                                                                         (self._x + self._width-1, self._y + self._height-1),
                                                                         (self._x, self._y + self._height-1)))

            return button

        def get_element(self):
            return self._particle

        def set_active(self):
            self._active = True

        def set_inactive(self):
            self._active = False

        def get_enabled(self):
            return self._enabled

        def set_enabled(self, status):
            self._enabled = status

        enabled = property(get_enabled, set_enabled)

        def get_lock(self):
            return self._unlocked

        def set_lock(self, status):
            self._unlocked = status

        unlocked = property(get_lock, set_lock)

        def contains(self, x, y):
            if x < self._x or self._x + self._width < x:
                return False

            if y < self._y or self._y + self._height < y:
                return False

            return True
