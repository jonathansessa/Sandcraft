import pygame
from particle_data import ELEMENTS

element_buttons = []


class ElementMenu:
    def __init__(self, surface, x, y, width):
        self._surface = surface
        self._x = x
        self._y = y
        self._width = width
        self._height = 0
        self.draw()

    def draw(self):
        sect_x = self._x
        sect_y = self._y
        sect_w = (self._width / 2) - 9
        for category in ELEMENTS:
            new_section = ElementSection(self._surface, sect_x, sect_y, sect_w, category, ELEMENTS[category])
            sect_x += sect_w + 10
            if sect_x > self._x + self._width:
                sect_x = self._x
                sect_y += new_section.get_height() + 20
        self._height = sect_y - self._y

    def update(self, driver, x, y):
        for button in element_buttons:
            button.set_inactive()
            if button.contains(x, y):
                button.set_active()
                driver.set_current_element(button.get_element())
            button.update()

    def contains(self, x, y):
        if x < self._x or self._x + self._width < x:
            return False
        if y < self._y or self._y + self._height < y:
            return False
        return True


class ElementSection:
    def __init__(self, surface, x, y, width, title, elements):
        self._surface = surface
        self._x = x
        self._y = y
        self._width = width
        self._height = 0
        self._title = title
        self._elements = elements
        self.draw()

    def draw(self):
        font = pygame.font.Font("fonts/RetroGaming.ttf", 11)
        t = font.render(self._title, True, pygame.Color(255, 255, 255))
        self._surface.blit(t, (self._x, self._y))

        top = self._y + 11 + 7
        left = self._x

        for e in self._elements:
            new_button = ElementButton(self._surface, left, top, 16, 16, e)
            left += 20

        self._height = 11 + 7 + 15

    def get_height(self):
        return self._height

    def contains(self, x, y):
        if x < self._x or self._x + self._width < x:
            return False

        if y < self._y or self._y + self._height < y:
            return False

        return True


class ElementButton:
    def __init__(self, surface, x, y, width, height, template_particle):
        self._surface = surface
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._particle = template_particle
        self._active = False
        self._enabled = True
        self._unlocked = True
        self.update()
        element_buttons.append(self)

    # Redraws button, returns bounding Rect for refresh
    def update(self):
        button = pygame.Rect(self._x, self._y, self._width, self._height)

        # If element is locked draw a black square with a question mark, otherwise draw square with element color
        if not self._unlocked:
            pygame.draw.rect(self._surface, (0, 0, 0), button)
            font = pygame.font.Font("fonts/RetroGaming.ttf", 11)
            q_mark = font.render("?", True, pygame.Color(255, 255, 255))
            self._surface.blit(q_mark, (self._x + 4, self._y + 1))
        else:
            pygame.draw.rect(self._surface, self._particle.color, button)

        # If element is not enabled, draw a semi-transparent white square over it
        if not self._enabled:
            s = pygame.Surface((self._width, self._height), pygame.SRCALPHA)
            s.fill((150, 150, 150, 180))
            self._surface.blit(s, (self._x, self._y))

        # If element is currently active/selected, draw a white line around button
        if self._active:
            pygame.draw.lines(self._surface, (255, 0, 0), True, ((self._x, self._y),
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

    def set_enabled(self):
        self._enabled = True

    def set_disabled(self):
        self._enabled = False

    def contains(self, x, y):
        if x < self._x or self._x + self._width < x:
            return False

        if y < self._y or self._y + self._height < y:
            return False

        return True

