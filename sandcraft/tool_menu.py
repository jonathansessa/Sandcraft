import pygame
import sys
from config import *


class ToolMenu:
    def __init__(self, surface, x, y, width):
        self._surface = surface
        self._x = x
        self._y = y
        self._width = width
        self._height = 100
        self._TOOLS = ["ADD", "DELETE", "ERASE", "LINE", "RECT", "OVAL", "INSPECT", "CLEAR", "SAVE", "LOAD", "QUIT"]
        self.tool_buttons = []
        self.draw()

    def draw(self):
        button_x = self._x
        button_y = self._y
        for tool in self._TOOLS:
            new_button = self.ToolButton(self._surface, button_x, button_y, tool)

            # If new button is outside of tool menu
            if button_x + new_button.get_width() > self._x + self._width:
                pygame.draw.rect(self._surface, BG_COLOR,
                                 pygame.Rect(button_x, button_y, new_button.get_width(), new_button.get_height()))
                button_x = self._x
                button_y = self._y + new_button.get_height() + 10
                new_button = self.ToolButton(self._surface, button_x, button_y, tool)

            button_x += new_button.get_width() + 10
            self.tool_buttons.append(new_button)

        self.draw_adjustment(1)

    # Checks if a button was clicked, then changes corresponding button to active
    def update(self, driver, x, y):
        for b in self.tool_buttons:
            if b.contains(x, y):
                for button in self.tool_buttons:
                    button.set_inactive()
                    if button.contains(x, y):
                        if button.get_tool() in ["ADD", "DELETE", "ERASE", "LINE", "RECT", "OVAL", "INSPECT"]:
                            button.set_active(driver)
                        elif button.get_tool() == "CLEAR":
                            driver.clear_sandbox()
                        elif button.get_tool() == "SAVE":
                            driver.save_state()
                        elif button.get_tool() == "LOAD":
                            driver.load_state()
                        elif button.get_tool() == "QUIT":
                            pygame.quit()
                            sys.exit()
                        elif button.get_tool() == "-":
                            driver.set_size(-1)
                            self.update_tool_size(driver)
                        elif button.get_tool() == "+":
                            driver.set_size(1)
                            self.update_tool_size(driver)
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
        self._surface.blit(label, (self._x, self._y + 70))

    def draw_adjustment(self, tool_size):
        top = self._y + 70
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
                pygame.draw.lines(self._surface, (255, 0, 0), True, ((self._x, self._y),
                                                                         (self._x + self._width-1, self._y),
                                                                         (self._x + self._width-1, self._y + self._height-1),
                                                                         (self._x, self._y + self._height-1)))
            else:
                pygame.draw.lines(self._surface, (0, 0, 0), True, ((self._x, self._y),
                                                                     (self._x + self._width - 1, self._y),
                                                                     (self._x + self._width - 1,
                                                                      self._y + self._height - 1),
                                                                     (self._x, self._y + self._height - 1)))

        def get_width(self):
            return self._width

        def get_height(self):
            return self._height

        def get_tool(self):
            return self._name

        def set_active(self, driver):
            self._active = True
            driver.set_tool(self._name)

        def set_inactive(self):
            self._active = False

        def contains(self, x, y):
            if x < self._x or self._x + self._width < x:
                return False

            if y < self._y or self._y + self._height < y:
                return False

            return True
