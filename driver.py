import pygame
from config import PARTICLE_SIZE
from grid import Grid
from painter import Painter
from particle_data import *


class Driver:
    def __init__(self):
        self.__particles = []
        self.__grid = Grid()
        self.__painter = Painter(template_sand)
        self.__tool = "ADD"
        self.__size = 1

    """
        add adds the specified particle both the particle list and the Grid the particle into the grid.
        This is the method that should be called when adding a particle to the Grid, NOT Grid.emplace
    """
    def add(self, particle):
        self.__particles.append(particle)
        self.__grid.emplace(particle)

    def set_tool(self, tool):
        self.__tool = tool

    def get_tool(self):
        return self.__tool

    def get_size(self):
        return self.__size

    def set_size(self, value):
        self.__size += value
        if self.__size < 1:
            self.__size = 1
        if self.__size > 6:
            self.__size = 6

    def clear_sandbox(self):
        self.__particles.clear()
        self.__grid = Grid()

    def draw_tool_outline(self, pos, sandbox, display):
        size = self.__size * PARTICLE_SIZE
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

    def update_on_tick(self, pygame_mouse):
        i = 0

        while i < len(self.__particles):
            self.__particles[i].update_on_tick(self, self.__grid)

            if self.__particles[i].is_live is False:
                self.__particles[i] = None
                self.__particles.pop(i)
            else:
                i += 1

        self.__painter.update_on_tick(pygame_mouse, self, self.__grid)

    """
        For now, you can select a particle by pressing these keys:
            1: sand     (solid)
            2: water    (liquid)
            3: lava     (liquid)
            4: steam    (gas)
            5: wood     (fixed)
        This functionality should be replaced with a particle picker UI, or something of the sort.
    """
    def update_on_key_down(self, pygame_event):
        if pygame_event.key == pygame.K_1:
            self.__painter.set_template_particle(template_sand)
        elif pygame_event.key == pygame.K_2:
            self.__painter.set_template_particle(template_water)
        elif pygame_event.key == pygame.K_3:
            self.__painter.set_template_particle(template_lava)
        elif pygame_event.key == pygame.K_4:
            self.__painter.set_template_particle(template_steam)
        elif pygame_event.key == pygame.K_5:
            self.__painter.set_template_particle(template_wood)

    def get_current_element(self):
        return self.__painter.get_template_particle()

    def set_current_element(self, new):
        self.__painter.set_template_particle(new)

    def render(self, screen):
        for particle in self.__particles:
            particle.render(screen)
