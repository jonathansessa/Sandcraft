import pygame
import math
from config import PARTICLE_SIZE
from grid import Grid, px_to_cell
from painter import Painter
from particle_data import *


class Driver:
    def __init__(self):
        self.__particles = []
        self.__grid = Grid()
        self.__painter = Painter(template_sand)
        self._tool = "ADD"
        self._size = 1
        self._tool_use = False
        self._line_start = (0, 0)
        self._line_end = (0, 0)
        self._line_active = False

    """
        add adds the specified particle both the particle list and the Grid the particle into the grid.
        This is the method that should be called when adding a particle to the Grid, NOT Grid.emplace
    """
    def add(self, particle):
        self.__particles.append(particle)
        self.__grid.emplace(particle)

    def delete(self, particle):
        try:
            self.__particles.remove(particle)
            self.__grid.remove(particle)
            for p in self.__grid.get_near((particle.col, particle.row)):
                p.force_update()
        except ValueError:
            pass

    def get_tool(self):
        return self._tool

    def set_tool(self, tool):
        self._tool = tool

    def get_size(self):
        return self._size

    # Boolean for if tool is active
    def set_tool_use(self, status):
        self._tool_use = status

    # Changes brush size with min, max value
    def set_size(self, value):
        self._size += value
        if self._size < 1:
            self._size = 1
        if self._size > 6:
            self._size = 6

    def clear_sandbox(self):
        self.__particles.clear()
        self.__grid = Grid()

    # Draws gray square outline instead of mouse, clips so not drawn outside sandbox
    def draw_tool_outline(self, pos, sandbox, display):
        if self._tool == "INSPECT":
            size = PARTICLE_SIZE

            x = px_to_cell(pos[0])
            y = px_to_cell(pos[1])

            font = pygame.font.Font("fonts/RetroGaming.ttf", 11)
            if self.__grid.exists((x, y)):
                current = self.__grid.get((x, y))
                label = font.render(f"{current.name}: {x}, {y}", True, (255, 255, 255), (0, 0, 0))
            else:
                label = font.render(f"Empty: {x}, {y}", True, (255, 255, 255), (0, 0, 0))
            label.set_clip(sandbox)
            display.blit(label, (pos[0]+10, pos[1]))
        else:
            size = self._size * PARTICLE_SIZE

        s1 = sandbox.clipline(pos[0], pos[1], pos[0] + size, pos[1])
        s2 = sandbox.clipline(pos[0] + size, pos[1], pos[0] + size, pos[1] + size)
        s3 = sandbox.clipline(pos[0] + size, pos[1] + size, pos[0], pos[1] + size)
        s4 = sandbox.clipline(pos[0], pos[1] + size, pos[0], pos[1])
        if s1:
            pygame.draw.line(display, (100, 100, 100), s1[0], s1[1])
        if s2:
            pygame.draw.line(display, (100, 100, 100), s2[0], s2[1])
        if s3:
            pygame.draw.line(display, (100, 100, 100), s3[0], s3[1])
        if s4:
            pygame.draw.line(display, (100, 100, 100), s4[0], s4[1])

    def start_line(self, pos):
        self._line_start = pos
        self._line_active = True

    def end_line(self, pos):
        self._line_end = pos
        self._line_active = False
        self.draw_line()

    def draw_line(self):
        (x, y) = (self._line_start[0], self._line_start[1])
        (p2, p2) = (px_to_cell(self._line_end[0]), px_to_cell(self._line_end[1]))

        if not self.__grid.is_in_bounds([p2, p2]):
            return

        r = math.atan2((self._line_end[1] - self._line_start[1]), (self._line_end[0] - self._line_start[0]))
        d = math.floor(math.sqrt((self._line_end[0] - self._line_start[0])**2 + (self._line_end[1] - self._line_start[1])**2))

        for i in range(d):
            x = self._line_start[0] + (i * math.cos(r))
            y = self._line_start[1] + (i * math.sin(r))

            (px, py) = (px_to_cell(x), px_to_cell(y))
            if self.__grid.exists([px, py]) is False:
                self.add(self.__painter.get_template_particle().clone(px, py))

    # For each particle, update its position. Then, apply tool if active
    def update_particles(self, mouse, sandbox, display):
        for particle in self.__particles:
            particle.update_on_tick(self, self.__grid)

            if particle.is_live is False:
                self.__particles.remove(particle)

        if self._tool_use:
            if self._tool == "LINE" and self._line_active:
                line = sandbox.clipline(self._line_start[0], self._line_start[1], mouse.get_pos()[0], mouse.get_pos()[1])
                pygame.draw.line(display, (100, 100, 100), line[0], line[1])
            elif self._tool == "ADD" or self._tool == "DELETE":
                self.__painter.use_tool(mouse, self, self.__grid)

    def get_current_element(self):
        return self.__painter.get_template_particle()

    def set_current_element(self, new):
        self.__painter.set_template_particle(new)

    def render(self, screen):
        for particle in self.__particles:
            particle.render(screen)
