from grid import px_to_cell


class Painter:
    def __init__(self, template_particle):
        self.__temp = template_particle

    def use_tool(self, pygame_mouse, driver, grid):
        mouse_col = px_to_cell(pygame_mouse.get_pos()[0])
        mouse_row = px_to_cell(pygame_mouse.get_pos()[1])

        # Add particles to grid based on tool size
        for x in range(mouse_col, mouse_col + driver.get_size()):
            for y in range(mouse_row, mouse_row + driver.get_size()):
                if grid.is_in_bounds([x, y]):
                    if grid.exists([x, y]) is False and driver.get_tool() == "ADD":
                        driver.add(self.__temp.clone(x, y))
                    elif grid.exists([x, y]) is True and driver.get_tool() == "DELETE":
                        driver.delete(grid.get([x, y]))

    def set_template_particle(self, template_particle):
        self.__temp = template_particle

    def get_template_particle(self):
        return self.__temp
