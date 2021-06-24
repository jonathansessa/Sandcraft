import os
import time
import pickle
import pygame
from config import PARTICLE_SIZE, SANDBOX_WIDTH, WINDOW_HEIGHT, SANDBOX_Y
from grid import Grid
from painter import Painter
from particle_data import *
from particle import Particle


class Driver:
    def __init__(self):
        self.__particles = []
        self.__grid = Grid()
        self.__painter = Painter(template_sand)
        self._tool = "ADD"
        self._size = 1
        self._tool_use = False

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

    # For each particle, update its position. Then, apply tool if active
    def update_particles(self, mouse):
        for particle in self.__particles:
            particle.update_on_tick(self, self.__grid)

            if particle.is_live is False:
                self.__particles.remove(particle)

        if self._tool_use:
            self.__painter.use_tool(mouse, self, self.__grid)

    def get_current_element(self):
        return self.__painter.get_template_particle()

    def set_current_element(self, new):
        self.__painter.set_template_particle(new)

    def render(self, screen):
        for particle in self.__particles:
            particle.render(screen)

    def save_state(self, screen):
        os.makedirs(os.path.dirname('./data/'), exist_ok=True)
        curr = time.time()
        with open('data/sc_state_%d.pickle' % curr, 'wb') as file:
            pickle.dump(self.__particles, file)
        self.print_message(screen, 'Saved!')

    def load_state(self, screen):
        if os.path.exists('./data/'):
            self.print_message(screen, 'Loading...')
            recent = 0
            for filename in os.listdir('./data/'):
                f = os.path.join('data', filename)
                if os.path.isfile(f) and filename.split('.')[-1] == 'pickle':  # check for pickle file
                    try:
                        timestamp = int(filename.split('.')[-2].split('_')[-1])
                        recent = timestamp if timestamp > recent else recent  # grab most recent file
                    except ValueError or IndexError:
                        continue
            if recent != 0:
                with open('data/sc_state_%d.pickle' % recent, 'rb') as file:
                    particles = pickle.load(file)
                    try:
                        self.clear_sandbox()
                        for particle in particles:
                            if isinstance(particle, Particle):
                                self.add(particle)
                            else:
                                raise ValueError
                        self.print_message(screen, 'Success: Loaded!')
                    except ValueError:
                        self.print_message(screen, 'Error: Invalid file data!')
            else:
                self.print_message(screen, 'Error: No state files detected!')
        else:
            self.print_message(screen, 'Error: Data directory does not exist!')

    def print_message(self, screen, text):
        print_font = pygame.font.Font("fonts/RetroGaming.ttf", 22)
        text_rect = print_font.render(text, True, pygame.Color(255, 255, 255))
        screen.blit(text_rect, text_rect.get_rect().move(
            (SANDBOX_WIDTH / 2 - text_rect.get_width() / 2, WINDOW_HEIGHT - SANDBOX_Y)))
