import os
import time
import pickle
import pygame
import math
from .config import *
from .grid import Grid, px_to_cell
from .painter import Painter
from .particle_data import *
from .particle import Particle
from .gas import Gas


def print_state_message(screen, text):
    # Clear previous message
    clear_surf = pygame.Surface((SANDBOX_WIDTH, (WINDOW_HEIGHT - SANDBOX_HEIGHT) / 2))
    clear_surf.fill(BG_COLOR)
    screen.blit(clear_surf, clear_surf.get_rect().move(
        (SANDBOX_WIDTH / 2 - clear_surf.get_width() / 2, WINDOW_HEIGHT - 2 * SANDBOX_Y)))

    # Print new message
    print_font = pygame.font.Font(FONT_PATH, 20)
    text_rect = print_font.render(text, True, pygame.Color(255, 255, 255))
    screen.blit(text_rect, text_rect.get_rect().move(
        (SANDBOX_WIDTH / 2 - text_rect.get_width() / 2, WINDOW_HEIGHT - 2 * SANDBOX_Y)))


class Driver:
    def __init__(self, mode, element_menu):
        self.__particles = []
        self.__grid = Grid()
        self.__painter = Painter(template_sand)
        self._mode = mode
        self._tool = "ADD"
        self._size = 1
        self._tool_use = False
        self._shape_start = (0, 0)
        self._shape_end = (0, 0)
        self._shape_active = False
        self.undiscovered = []
        self.__element_menu = element_menu

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
        if self._tool == "LINE" and self._shape_active:
            r = math.atan2((pos[1] - self._shape_start[1]), (pos[0] - self._shape_start[0])) + math.radians(90)
            width = self._size * PARTICLE_SIZE

            s1 = sandbox.clipline(self._shape_start[0], self._shape_start[1], pos[0], pos[1])
            s2 = sandbox.clipline(pos[0], pos[1], pos[0] + (width * math.cos(r)), pos[1] + (width * math.sin(r)))
            s3 = sandbox.clipline(self._shape_start[0], self._shape_start[1], self._shape_start[0] +
                                  (width * math.cos(r)), self._shape_start[1] + (width * math.sin(r)))
            s4 = sandbox.clipline(self._shape_start[0] + (width * math.cos(r)), self._shape_start[1] +
                                  (width * math.sin(r)), pos[0] + (width * math.cos(r)), pos[1] +
                                  (width * math.sin(r)))

        elif self._tool == "RECT" and self._shape_active:
            (x1, y1) = (self._shape_start[0], self._shape_start[1])
            (x2, y2) = (pos[0], pos[1])

            s1 = sandbox.clipline(x1, y1, x1, y2)
            s2 = sandbox.clipline(x1, y2, x2, y2)
            s3 = sandbox.clipline(x2, y2, x2, y1)
            s4 = sandbox.clipline(x2, y1, x1, y1)

        else:
            if self._tool == "INSPECT":
                size = PARTICLE_SIZE

                x = px_to_cell(pos[0])
                y = px_to_cell(pos[1])

                font = pygame.font.Font(FONT_PATH, 11)
                if self.__grid.exists((x, y)):
                    current = self.__grid.get((x, y))
                    label = font.render(f"{current.name}: {x}, {y}", True, (255, 255, 255), (0, 0, 0))
                else:
                    label = font.render(f"Empty: {x}, {y}", True, (255, 255, 255), (0, 0, 0))
                label.set_clip(sandbox)
                display.blit(label, (pos[0]+10, pos[1]))
            # Draw tool for add/delete
            else:
                size = self._size * PARTICLE_SIZE

            s1 = sandbox.clipline(pos[0], pos[1], pos[0] + size, pos[1])
            s2 = sandbox.clipline(pos[0] + size, pos[1], pos[0] + size, pos[1] + size)
            s3 = sandbox.clipline(pos[0] + size, pos[1] + size, pos[0], pos[1] + size)
            s4 = sandbox.clipline(pos[0], pos[1] + size, pos[0], pos[1])

        # Draw tool outlines (if they exist)
        if s1:
            pygame.draw.line(display, (100, 100, 100), s1[0], s1[1])
        if s2:
            pygame.draw.line(display, (100, 100, 100), s2[0], s2[1])
        if s3:
            pygame.draw.line(display, (100, 100, 100), s3[0], s3[1])
        if s4:
            pygame.draw.line(display, (100, 100, 100), s4[0], s4[1])

    def start_shape(self, pos):
        self._shape_start = pos
        self._shape_active = True

    def end_line(self, pos):
        self._shape_end = pos
        self._shape_active = False
        self.draw_line()

    def end_rect(self, pos):
        self._shape_end = pos
        self._shape_active = False
        self.draw_rect()

    def draw_line(self):
        (p2, p2) = (px_to_cell(self._shape_end[0]), px_to_cell(self._shape_end[1]))

        if not self.__grid.is_in_bounds([p2, p2]):
            return

        r = math.atan2((self._shape_end[1] - self._shape_start[1]), (self._shape_end[0] - self._shape_start[0]))
        r2 = r + math.radians(90)
        d = math.floor(math.sqrt((self._shape_end[0] - self._shape_start[0])**2 +
                                 (self._shape_end[1] - self._shape_start[1])**2))
        w = self._size * PARTICLE_SIZE

        for i in range(d):
            for j in range(w):
                x = self._shape_start[0] + (i * math.cos(r)) + (j * math.cos(r2))
                y = self._shape_start[1] + (i * math.sin(r)) + (j * math.sin(r2))

                (px, py) = (px_to_cell(x), px_to_cell(y))
                if self.__grid.exists([px, py]) is False:
                    self.add(self.__painter.get_template_particle().clone(px, py))

    def draw_rect(self):
        (p1x, p1y) = (px_to_cell(self._shape_start[0]), px_to_cell(self._shape_start[1]))
        (p2x, p2y) = (px_to_cell(self._shape_end[0]), px_to_cell(self._shape_end[1]))

        if p2x < p1x:
            temp = p1x
            p1x = p2x
            p2x = temp

        if p2y < p1y:
            temp = p1y
            p1y = p2y
            p2y = temp

        if not self.__grid.is_in_bounds([p2x, p2y]):
            return

        for i in range(p1x, p2x+1):
            for j in range(p1y, p2y+1):
                if self.__grid.exists([i, j]) is False:
                    self.add(self.__painter.get_template_particle().clone(i, j))

    # For each particle, update its position. Then, apply tool if active
    def update_particles(self, mouse, sandbox, display):
        for particle in self.__particles:
            particle.update_on_tick(self, self.__grid)

            if particle.is_live is False:
                self.__particles.remove(particle)

        if self._tool_use:
            if self._tool == "ADD" or self._tool == "DELETE":
                self.__painter.use_tool(mouse, self, self.__grid)

    def get_current_element(self):
        return self.__painter.get_template_particle()

    def set_current_element(self, new):
        self.__painter.set_template_particle(new)

    # Draws particles in sandbox, also checks for new elements in Discovery Mode
    def render(self, screen):
        for particle in self.__particles:
            particle.render(screen)

            if self._mode == "DISCOVERY" and len(self.undiscovered) != 0:
                if particle.name == "Steam":
                    for e in self.__element_menu.element_buttons:
                        if e.get_element() == template_steam:
                            e.unlocked = True
                            e.update()
                            try:
                                for elem in self.undiscovered:
                                    if elem.name == "Steam":
                                        self.undiscovered.remove(elem)
                                # self.undiscovered.remove(template_steam)
                            except ValueError:
                                continue

                            click = False
                            while not click:
                                font = pygame.font.Font(FONT_PATH, 30)
                                alert = font.render("STEAM DISCOVERED!", False, (255, 255, 255))
                                alert_rect = alert.get_rect()
                                alert_rect.center = (SANDBOX_WIDTH / 2, SANDBOX_HEIGHT / 2)
                                screen.blit(alert, alert_rect)

                                font2 = pygame.font.Font(FONT_PATH, 18)
                                alert2 = font2.render("(Click to Continue)", False, (255, 255, 255))
                                alert2_rect = alert2.get_rect()
                                alert2_rect.center = (SANDBOX_WIDTH / 2, (SANDBOX_HEIGHT / 2) + 50)
                                screen.blit(alert2, alert2_rect)

                                pygame.display.update()

                                for event in pygame.event.get():
                                    if event.type == pygame.MOUSEBUTTONDOWN:
                                        click = True
                                    if event.type == pygame.KEYDOWN:
                                        click = True

    def save_state(self, screen):
        os.makedirs(os.path.dirname('./data/'), exist_ok=True)
        curr = time.time()
        for particle in self.__particles:
            if isinstance(particle, Gas):
                particle.save_lifespan()
        data = {
            'particles': self.__particles,
            'undiscovered': self.undiscovered
        }
        with open('data/sc_state_%s_%d.pickle' % (self._mode, curr), 'wb') as file:
            pickle.dump(data, file)
        print_state_message(screen, 'Saved!')

    def load_state(self, screen):
        if os.path.exists('./data/'):
            print_state_message(screen, 'Loading...')
            recent = 0
            for filename in os.listdir('./data/'):
                f = os.path.join('data', filename)
                if os.path.isfile(f) and filename.split('.')[-1] == 'pickle'\
                        and filename.split('.')[-2].split('_')[-2] == self._mode:  # check for pickle file
                    try:
                        timestamp = int(filename.split('.')[-2].split('_')[-1])
                        recent = timestamp if timestamp > recent else recent  # grab most recent file
                    except ValueError or IndexError:
                        continue
            if recent != 0:
                with open('data/sc_state_%s_%d.pickle' % (self._mode, recent), 'rb') as file:
                    try:
                        data = pickle.load(file)
                        self.clear_sandbox()
                        for particle in data['particles']:
                            if isinstance(particle, Particle):
                                if isinstance(particle, Gas):
                                    particle.load_lifespan()
                                self.add(particle)
                            else:
                                raise ValueError
                        if self._mode == "DISCOVERY":
                            self.undiscovered = data['undiscovered']
                            for e in self.__element_menu.element_buttons:
                                if e.get_element().name in [element.name for element in self.undiscovered]:
                                    e.unlocked = False
                                else:
                                    e.unlocked = True
                                e.update()
                        print_state_message(screen, 'Success: Loaded!')
                    except:
                        print_state_message(
                            screen, 'Error: sc_state_%s_%d contains invalid data!' % (self._mode, recent))
            else:
                print_state_message(screen, 'Error: No state files detected!')
        else:
            print_state_message(screen, 'Error: Data directory does not exist!')
