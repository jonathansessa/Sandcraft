from sandcraft.solid_body import SolidBody


class BasicSolidBody(SolidBody):
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
        return BasicSolidBody(
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
        self._update_position(grid)

    def _update_position(self, grid):
        can_move = True

        for row in range(self._height):
            for col in range(self._width):
                if self._particles[row][col] is None:
                    continue
                particle = self._particles[row][col]
                pos_probe = (particle.col + self._true_vel_x(), particle.row + self._true_vel_y())
                particle_probe = grid.get(pos_probe)
                if particle_probe is not None and self.contains(particle_probe):
                    continue
                else:
                    if not grid.is_in_bounds(pos_probe) or grid.exists(pos_probe):
                        can_move = False
                        break
            if not can_move:
                break

        if can_move:
            self._col += self._true_vel_x()
            self._row += self._true_vel_y()

            probe_dir_x = 1
            probe_start_col = 0
            probe_end_col = self._width

            probe_dir_y = -1
            probe_start_row = self._height - 1
            probe_end_row = -1

            if self._vel_x > 0.0:
                probe_dir_x = -1
                probe_start_col = self._width - 1
                probe_end_col = -1

            if self._vel_y < 0.0:
                probe_dir_y = 1
                probe_start_row = 0
                probe_end_row = self._height

            for row in range(probe_start_row, probe_end_row, probe_dir_y):
                for col in range(probe_start_col, probe_end_col, probe_dir_x):
                    if self._particles[row][col] is None:
                        continue
                    particle = self._particles[row][col]
                    pos = (particle.col, particle.row)
                    pos_new = (particle.col + self._true_vel_x(), particle.row + self._true_vel_y())
                    grid.swap(pos, pos_new)

        return can_move
