import pickle
import tkinter as tk
from tkinter import filedialog
from sandcraft.config import *
from sandcraft.grid import Grid, px_to_cell
from sandcraft.painter import Painter
from sandcraft.particle_data import *
from sandcraft.particle import Particle
from sandcraft.gas import Gas
from sandcraft.music_mixer import MusicMixer


def print_state_message(screen, text):
    # Clear previous message
    clear_surf = pygame.Surface((SANDBOX_WIDTH, (WINDOW_HEIGHT - SANDBOX_HEIGHT) / 2))
    clear_surf.fill(BG_COLOR)
    screen.blit(clear_surf, clear_surf.get_rect().move(
        (SANDBOX_WIDTH / 2 - clear_surf.get_width() / 2, WINDOW_HEIGHT - 1.25 * SANDBOX_Y)))

    # Print new message
    print_font = pygame.font.Font(FONT_PATH, 20)
    text_rect = print_font.render(text, False, (255, 255, 255))
    screen.blit(text_rect, text_rect.get_rect().move(
        (SANDBOX_WIDTH / 2 - text_rect.get_width() / 2, WINDOW_HEIGHT - 1.25 * SANDBOX_Y)))


class Driver:
    def __init__(self, mode, element_menu, display):
        self.__particles = []
        self.__solid_bodies = []
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
        self.__display = display

        # Initializes and clears Tkinter window, allows for filedialog
        root = tk.Tk()
        root.withdraw()

        #initializing music player
        self.__musicPlayer = MusicMixer()

        if mode == 'LOAD':
            self.load_state()

    """
        add adds the specified particle both the particle list and the Grid the particle into the grid.
        This is the method that should be called when adding a particle to the Grid, NOT Grid.emplace
    """
    def add(self, particle):
        self.__particles.append(particle)
        self.__grid.emplace(particle)

    def add_list(self, particle_list):
        for particle in particle_list:
            if particle is not None:
                self.add(particle)

    def add_solid_body(self, solid_body):
        self.__solid_bodies.append(solid_body)

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

    def end_active_shape(self):
        self._shape_active = False

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

    def clear_element(self):
        selected_elem = None
        for elem in self.__element_menu.element_buttons:
            if elem.active:
                selected_elem = elem.particle
                break
        if selected_elem is None:
            return
        while selected_elem.name in [elem.name for elem in self.__particles]:
            for particle in self.__particles:
                if particle.name == selected_elem.name:
                    try:
                        self.__particles.remove(particle)
                        self.__grid.remove(particle)
                        for p in self.__grid.get_near((particle.col, particle.row)):
                            p.force_update()
                    except ValueError:
                        pass

    # Draws gray square outline instead of mouse, clips so not drawn outside sandbox
    def draw_tool_outline(self, pos, sandbox, display):
        line_color = (100, 100, 100)

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

        elif self._tool == "OVAL" and self._shape_active:
            (x1, y1) = (self._shape_start[0], self._shape_start[1])
            (x2, y2) = (pos[0], pos[1])
            width, height = abs(x2 - x1), abs(y2 - y1)

            shape = pygame.Rect(min(x1, x2), min(y1, y2), width, height)
            pygame.draw.ellipse(display, line_color, shape, 1)

            return
        else:
            if self._tool == "INSPECT":
                size = PARTICLE_SIZE
                x, y = px_to_cell(pos[0]), px_to_cell(pos[1])

                font = pygame.font.Font(FONT_PATH, 11)
                if self.__grid.exists((x, y)):
                    particle = self.__grid.get((x, y))
                    label = font.render(f"{particle.name}: {x}, {y} Temp: {str(round(particle.temp, 1))} C",
                                        True, (255, 255, 255), (0, 0, 0))
                else:
                    label = font.render(f"Empty: {x}, {y}", True, (255, 255, 255), (0, 0, 0))

                # Adjust label location depending on proximity to edge of Sandbox
                x_offset, y_offset = 10, 5
                if pos[0] > SANDBOX_WIDTH * 0.75:
                    x_offset = -label.get_width() - 10
                if pos[1] > SANDBOX_HEIGHT * 0.95:
                    y_offset = -label.get_height() - 5

                display.blit(label, (pos[0] + x_offset, pos[1] + y_offset))

            # Draw tool for add/delete
            else:
                size = self._size * PARTICLE_SIZE

            # Create lines for square, cropped by Sandbox
            s1 = sandbox.clipline(pos[0], pos[1], pos[0] + size, pos[1])
            s2 = sandbox.clipline(pos[0] + size, pos[1], pos[0] + size, pos[1] + size)
            s3 = sandbox.clipline(pos[0] + size, pos[1] + size, pos[0], pos[1] + size)
            s4 = sandbox.clipline(pos[0], pos[1] + size, pos[0], pos[1])

        # Draw tool outlines (if they exist)
        if s1:
            pygame.draw.line(display, line_color, s1[0], s1[1])
        if s2:
            pygame.draw.line(display, line_color, s2[0], s2[1])
        if s3:
            pygame.draw.line(display, line_color, s3[0], s3[1])
        if s4:
            pygame.draw.line(display, line_color, s4[0], s4[1])

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

    def end_oval(self, pos):
        self._shape_end = pos
        self._shape_active = False
        self.draw_oval()

    # Ellipse collision detection solution from:
    # https://stackoverflow.com/questions/59971407/how-can-i-test-if-a-point-is-in-an-ellipse
    def draw_oval(self):
        width, height = abs(self._shape_end[0] - self._shape_start[0]), abs(self._shape_end[1] - self._shape_start[1])
        shape = pygame.Rect(min(self._shape_start[0], self._shape_end[0]),
                            min(self._shape_start[1], self._shape_end[1]), width, height)

        x1, y1, x2, y2 = shape.left, shape.top, shape.right, shape.bottom
        cx, cy = shape.centerx, shape.centery
        a = width // 2
        b = height // 2

        if a == 0 or b == 0:
            return
        scale = a / b

        for i in range(x1, x2 + 1):
            for j in range(y1, y2 + 1):
                dx = i - cx
                dy = (j - cy) * scale
                if dx*dx + dy*dy <= a*a:
                    (px, py) = (px_to_cell(i), px_to_cell(j))
                    if self.__grid.is_in_bounds([px, py]) and self.__grid.exists([px, py]) is False:
                        self.add(self.__painter.get_template_particle().clone(px, py))

    def draw_line(self):
        (p1, p2) = (px_to_cell(self._shape_end[0]), px_to_cell(self._shape_end[1]))

        if not self.__grid.is_in_bounds([p1, p2]):
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
    def update_particles(self, mouse):
        for solid_body in self.__solid_bodies:
            if solid_body.empty():
                self.__solid_bodies.remove(solid_body)
            else:
                solid_body.update_on_tick(self, self.__grid)

        for particle in self.__particles:
            particle.update_on_tick(self, self.__grid)

            if particle.is_live is False or self.__grid.exists([particle.col, particle.row]) is False:
                try:
                    self.__particles.remove(particle)
                except ValueError:
                    pass

            if particle.name == "Water Generator":
                particle.force_update()

        if self._tool_use:
            if self._tool == "ADD" or self._tool == "DELETE" or self._tool == "ERASE":
                self.__painter.use_tool(mouse, self, self.__grid)

    def get_current_element(self):
        return self.__painter.get_template_particle()

    def set_current_element(self, new):
        self.__painter.set_template_particle(new)

    # Draws particles in sandbox, also checks for new elements in Discovery Mode
    def render(self, screen):
        for particle in self.__particles:
            particle.render(screen)

            if self._mode == "DISCOVERY" and len(self.undiscovered) > 0 and particle.name in self.undiscovered:
                for e in self.__element_menu.element_buttons:
                    if e.get_element().name == particle.name:
                        e._unlocked = True
                        e.update()
                        for elem in self.undiscovered:
                            if elem == particle.name:
                                self.undiscovered.remove(elem)
                                break
                        self.__musicPlayer.ding_Discovery()
                        click = False
                        while not click:
                            font = pygame.font.Font(FONT_PATH, 30)
                            alert = font.render("%s DISCOVERED!" % particle.name.upper(), False, (255, 255, 255))
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
                        return

    def save_state(self):
        for particle in self.__particles:
            if isinstance(particle, Gas):
                particle.save_lifespan()
        data = {
            'particles': self.__particles,
            'undiscovered': self.undiscovered,
            'mode': self._mode
        }
        file_path = filedialog.asksaveasfilename(defaultextension='.pickle',
                                                 filetypes=[('Pickle Files', '*.pickle')])
        if file_path == '':  # if cancel button clicked
            return
        with open(file_path, 'wb') as file:
            pickle.dump(data, file)
        print_state_message(self.__display, 'Saved!')

    def load_state(self):
        file_path = filedialog.askopenfilename(title='Select a File',
                                               filetypes=[('Pickle Files', '*.pickle')])
        if file_path == '':  # if cancel button clicked
            return
        with open(file_path, 'rb') as file:
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

                if data['mode'] not in ["DISCOVERY", "SANDBOX"]:
                    raise ValueError
                elif data['mode'] == "DISCOVERY":
                    self.undiscovered = data['undiscovered']
                else:
                    self.undiscovered = []

                self.__element_menu.discovery_init(self.undiscovered)

                self._mode = data['mode']

                print_state_message(self.__display, 'Success: Loaded!')
            except:
                print_state_message(self.__display, 'Error: %s has invalid data!' % os.path.basename(file_path))

    @property
    def grid(self):
        return self.__grid
