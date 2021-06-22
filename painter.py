from grid import px_to_cell


class Painter:
    def __init__(self, template_particle):
        self.__temp = template_particle

    def update_on_tick(self, pygame_mouse, driver, grid):
        buttons = pygame_mouse.get_pressed(3)

        if buttons[0] is True and driver.get_tool() == "ADD":
            mouse_col = px_to_cell(pygame_mouse.get_pos()[0])
            mouse_row = px_to_cell(pygame_mouse.get_pos()[1])
            mouse_pos = (mouse_col, mouse_row)

            for x in range(mouse_col, mouse_col + driver.get_size()):
                for y in range(mouse_row, mouse_row + driver.get_size()):
                    if grid.is_in_bounds([x, y]) is True and grid.exists([x, y]) is False:
                        driver.add(self.__temp.clone(x, y))

    def set_template_particle(self, template_particle):
        self.__temp = template_particle

    def get_template_particle(self):
        return self.__temp
