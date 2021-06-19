import pygame

from grid import Grid
from painter import Painter
from particle_data import template_sand, template_water, template_lava, template_steam, template_wood


class Driver:
    def __init__(self):
        self.__particles = []
        self.__grid = Grid()
        self.__painter = Painter(template_sand)

    """
        add adds the specified particle both the particle list and the Grid the particle into the grid.
        This is the method that should be called when adding a particle to the Grid, NOT Grid.emplace
    """
    def add(self, particle):
        self.__particles.append(particle)
        self.__grid.emplace(particle)

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

    def render(self, screen):
        for particle in self.__particles:
            particle.render(screen)
