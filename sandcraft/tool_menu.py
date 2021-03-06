import pygame.mouse
from sandcraft.config import *


class ToolMenu:
    def __init__(self, surface, x, y, width):
        self._surface = surface
        self._x = x
        self._y = y
        self._width = width
        self._height = 100
        self.__tool_groups = {"TOOLS": ["ADD", "ERASE", "CLEAR", "REMOVE"],
                              "SHAPES": ["LINE", "RECT", "OVAL"],
                              "FILE": ["INSPECT", "SAVE", "LOAD", "EXIT"]}
        self.tool_buttons = []
        self._rows = 0
        self.draw()

    def draw(self):
        button_x = self._x
        button_y = self._y
        rows = 1
        for group in self.__tool_groups:
            font = pygame.font.Font(FONT_PATH, 11)
            label = font.render(group, True, pygame.Color(255, 255, 255))
            self._surface.blit(label, (button_x, button_y))
            button_y += label.get_height()

            offset_height = 0
            for tool in self.__tool_groups[group]:
                new_button = self.ToolButton(self._surface, button_x, button_y, tool)
                if tool == "ADD":
                    new_button.set_active(None)
                    new_button.update()
                button_x += new_button.get_width() + 10
                offset_height = new_button.get_height()
                self.tool_buttons.append(new_button)

            button_x = self._x
            button_y = offset_height + 10 + button_y
            rows += 1

        self.draw_adjustment(1, rows)
        self._rows = rows

    # Checks if a button was clicked, then changes corresponding button to active
    def update(self, driver, x, y, click):
        toggle_inactive = False
        for button in self.tool_buttons:
            if button.contains(x, y):
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                if click:
                    if button.get_tool() in ["ADD", "DELETE", "ERASE", "LINE", "RECT", "OVAL", "INSPECT"]:
                        toggle_inactive = True
                        button.set_active(driver)
                    elif button.get_tool() == "CLEAR":
                        driver.clear_sandbox()
                    elif button.get_tool() == "REMOVE":
                        driver.clear_element()
                    elif button.get_tool() == "SAVE":
                        driver.save_state()
                    elif button.get_tool() == "LOAD":
                        driver.load_state()
                    elif button.get_tool() == "EXIT":
                        pygame.event.post(TOMENU_EVENT)
                    elif button.get_tool() == "-":
                        driver.set_size(-1)
                        self.update_tool_size(driver)
                    elif button.get_tool() == "+":
                        driver.set_size(1)
                        self.update_tool_size(driver)
                else:
                    return
        if click:
            for button in self.tool_buttons:
                if not button.contains(x, y) and toggle_inactive:
                    button.set_inactive()
                button.update()

    def contains(self, x, y):
        if x < self._x or self._x + self._width < x:
            return False
        if y < self._y or self._y + self._height < y:
            return False
        return True

    def update_tool_size(self, driver):
        tool_size = driver.get_size()
        font = pygame.font.Font(FONT_PATH, 11)
        label = font.render(f"BRUSH SIZE: {tool_size} ", True, pygame.Color(255, 255, 255), BG_COLOR)
        top = self._y + 5 + 35 * self._rows
        left = self._x
        self._surface.blit(label, (left, top))

    def draw_adjustment(self, tool_size, rows):
        top = self._y + 5 + 35 * rows
        left = self._x

        font = pygame.font.Font(FONT_PATH, 11)
        label = font.render(f"BRUSH SIZE: {tool_size}", True, pygame.Color(255, 255, 255), BG_COLOR)
        self._surface.blit(label, (left, top))

        top += 20

        button = self.ToolButton(self._surface, left, top, "-")
        left += button.get_width() + 10
        self.tool_buttons.append(button)

        button = self.ToolButton(self._surface, left, top, "+")
        self.tool_buttons.append(button)

        self._height += 100

    class ToolButton:
        def __init__(self, surface, x, y, name):
            self._surface = surface
            self._x = x
            self._y = y
            self._width = 0
            self._height = 0
            self._name = name
            self._active = False
            self.create()
            self.update()

        # Redraws button, returns bounding Rect for refresh
        def create(self):
            font = pygame.font.Font(FONT_PATH, 11)
            label = font.render(self._name, True, pygame.Color(0, 0, 0))
            button = label.get_rect()
            button.update(self._x, self._y, button.width + 20, button.height + 10)

            self._width = button.width
            self._height = button.height

            pygame.draw.rect(self._surface, (180, 180, 180), button)
            self._surface.blit(label, (self._x + 10, self._y + 5))

        def update(self):
            if self._active:
                pygame.draw.lines(
                    self._surface, (255, 0, 0), True, ((self._x, self._y),
                                                       (self._x + self._width-1, self._y),
                                                       (self._x + self._width-1, self._y + self._height-1),
                                                       (self._x, self._y + self._height-1)))
            else:
                pygame.draw.lines(
                    self._surface, (0, 0, 0), True, ((self._x, self._y),
                                                     (self._x + self._width - 1, self._y),
                                                     (self._x + self._width - 1, self._y + self._height - 1),
                                                     (self._x, self._y + self._height - 1)))

        def get_width(self):
            return self._width

        def get_height(self):
            return self._height

        def get_tool(self):
            return self._name

        def set_active(self, driver):
            self._active = True
            if driver is not None:
                driver.set_tool(self._name)

        def set_inactive(self):
            self._active = False

        def contains(self, x, y):
            if x < self._x or self._x + self._width < x:
                return False

            if y < self._y or self._y + self._height < y:
                return False

            return True
