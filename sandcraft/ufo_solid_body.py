from sandcraft.basic_solid_body import BasicSolidBody


class UFOSolidBody(BasicSolidBody):
    def __init__(
            self,
            id_color_dict,
            id_2d_list,
            width, height,
            col, row,
            vel_x, vel_y,
            acc_x, acc_y,
            temp, temp_freeze, temp_boil,
            density,
            color,
            name,
            flammability,
            state):

        super().__init__(
            id_color_dict,
            id_2d_list,
            width, height,
            col, row,
            vel_x, vel_y,
            acc_x, acc_y,
            temp, temp_freeze, temp_boil,
            density,
            color,
            name,
            flammability,
            state)

    def clone(self, col, row):
        return UFOSolidBody(
            self._id_color_dict,
            self._id_2d_list,
            self._width, self._height,
            col, row,
            self._vel_x, self._vel_y,
            self._acc_x, self._acc_y,
            self._temp, self._temp_freeze, self._temp_boil,
            self._density,
            self._color,
            self._name,
            self._flammability,
            self._state)

    def update_on_tick(self, driver, grid):
        can_move = self._update_position(grid)
        if not can_move:
            self._vel_x = -self._vel_x
