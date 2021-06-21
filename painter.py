from grid import px_to_cell


class Painter:
    def __init__(self, template_particle):
        self.__temp = template_particle

    def update_on_tick(self, pygame_mouse, driver, grid):
        buttons = pygame_mouse.get_pressed(3)

        if buttons[0] is True:
            mouse_col = px_to_cell(pygame_mouse.get_pos()[0])
            mouse_row = px_to_cell(pygame_mouse.get_pos()[1])
            mouse_pos = (mouse_col, mouse_row)

            if grid.is_in_bounds(mouse_pos) is True and grid.exists(mouse_pos) is False:
                driver.add(self.__temp.clone(mouse_col, mouse_row))

    def set_template_particle(self, template_particle):
        self.__temp = template_particle

    def get_template_particle(self):
        return self.__temp
