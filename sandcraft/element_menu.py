import pygame
from sandcraft.config import FONT_PATH, BG_COLOR
from sandcraft.particle_data import ELEMENTS


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
        self._height = 150
        self._mode = mode
        self.element_buttons = []
        self.draw(True)

    # Creates the menu by building each section based on particle_data
    # Create flag determines whether button should be instantiated (false for redrawing section labels)
    def draw(self, create):
        sect_x = self._x
        sect_y = self._y
        sect_w = self._width / 2 - self.MARGIN
        for category in ELEMENTS.keys():
            self.create_section(self._surface, sect_x, sect_y, sect_w, category, ELEMENTS[category], create)
            sect_x += sect_w + self.MARGIN
            if sect_x >= self._x + self._width:
                sect_x = self._x
                sect_y += 50

    # First checks if a button was clicked, then changes corresponding button to active
    def update(self, driver, x, y):
        toggle = False
        for button in self.element_buttons:
            if button.contains(x, y) and button.unlocked:
                toggle = True
                driver.set_current_element(button.get_element())
            button.update()
        if toggle:
            for button in self.element_buttons:
                button.set_active(False)
                if button.contains(x, y) and button.unlocked:
                    button.set_active(True)
                button.update()

    def draw_tooltip(self, mouse_x, mouse_y):
        elem_menu_rect = pygame.Rect(self._x, self._y, self._width, self._height)
        pygame.draw.rect(self._surface, BG_COLOR, elem_menu_rect)
        self.draw(False)

        hovered = None
        for button in self.element_buttons:
            button.update()
            if button.contains(mouse_x, mouse_y) and button.unlocked:
                hovered = button
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
        if hovered is None:
            return

        font = pygame.font.Font(FONT_PATH, 11)
        label = font.render(f"{hovered.particle.name.upper()}", True, (255, 255, 255), (0, 0, 0))
        x_offset, y_offset = 15, 10
        self._surface.blit(label, (mouse_x + x_offset, mouse_y - y_offset))

    def contains(self, x, y):
        if x < self._x or self._x + self._width < x:
            return False
        if y < self._y or self._y + self._height < y:
            return False
        return True

    def create_section(self, surface, x, y, width, title, elements, create):
        t = self.FONT.render(title, True, self.FONT_COLOR)
        surface.blit(t, (x, y))

        left = x
        top = y + t.get_height() + self.MARGIN/2

        for e in elements:
            if create:
                new_button = self.ElementButton(surface, left, top, self.BUTTON_SIZE, self.BUTTON_SIZE, e)
                self.element_buttons.append(new_button)
                if e.name == "sand":
                    new_button.set_active(True)
                    new_button.update()
            left += self.BUTTON_SIZE + self.MARGIN
            if left + self.BUTTON_SIZE > x + width:
                left = x
                top += self.BUTTON_SIZE + self.MARGIN

        return top + self.BUTTON_SIZE - self._y

    def discovery_init(self, undiscovered):
        for button in self.element_buttons:
            if button.get_element().name in undiscovered:
                button._unlocked = False
            else:
                button._unlocked = True
            button.update()

    class ElementButton:
        ACTIVE_COLOR = (255, 0, 0)

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

        # Redraws button based on particle and if unlocked/enabled/active
        def update(self):
            button = pygame.Rect(self._x, self._y, self._width, self._height)

            # If element is locked draw a black square with a question mark, otherwise draw square with element color
            if not self._unlocked:
                pygame.draw.rect(self._surface, (0, 0, 0), button)
                font = pygame.font.Font(FONT_PATH, 11)
                q_mark = font.render("?", False, (255, 255, 255))
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
                pygame.draw.lines(self._surface, self.ACTIVE_COLOR, True,
                                  ((self._x, self._y),
                                   (self._x + self._width-1, self._y),
                                   (self._x + self._width-1, self._y + self._height-1),
                                   (self._x, self._y + self._height-1)))

            return button

        def get_element(self):
            return self._particle

        # def set_active(self):
        #     self._active = True
        #
        # def set_inactive(self):
        #     self._active = False

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

        def get_active(self):
            return self._active

        def set_active(self, active):
            self._active = active

        active = property(get_active, set_active)

        def get_particle(self):
            return self._particle

        def set_particle(self, particle):
            self._particle = particle

        particle = property(get_particle, set_particle)

        def contains(self, x, y):
            if x < self._x or self._x + self._width < x:
                return False

            if y < self._y or self._y + self._height < y:
                return False

            return True
