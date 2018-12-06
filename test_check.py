# check the check
class Grid(object):
    # in the format x, y OR col, row
    MOVE_CALCULATIONS = {
        'we': (-1, 0),
        'nw': (-1, -1),
        'no': (0, -1),
        'ne': (1, -1),
        'ea': (1, 0),
        'se': (1, 1),
        'so': (0, 1),
        'sw': (-1, 1),
    }

    def __init__(self, raw_grid_letters, size=(8, 8), value=True):
        self.raw_grid_letters = raw_grid_letters
        self.cols = size[0]
        self.rows = size[1]
        self.grid = self.generate_grid()
        self.grid_map = self.generate_grid_map(value=value)
        self.king_count = 0

    @property
    def max_col_index(self):
        _max_col_index = self.cols - 1
        return _max_col_index

    @property
    def max_row_index(self):
        _max_row_index = self.rows - 1
        return _max_row_index

    def generate_grid(self):
        raw_grid_letters = self.raw_grid_letters
        grid = []
        for _letters in raw_grid_letters:
            letters = [x for x in _letters]
            grid.append(letters)

        return grid

    def generate_grid_map(self, value=True):
        grid = self.grid
        grid_map = []
        for row in grid:
            grid_map_row = []
            for i in row:
                grid_map_row.append(value)

            grid_map.append(grid_map_row)

        return grid_map

    def scan(self, mode='initial'):
        grid = self.grid
        grid_map = self.grid_map

        if mode == 'initial':
            for i, grid_row in enumerate(grid):
                # break if king count is at least 2
                if self.king_count >= 2:
                    break

                for j, char in enumerate(grid_row):
                    king_value = 'k'
                    is_king = (char.lower() == king_value)
                    if is_king:
                        self.king_count += 1
                        grid_map[i][j] = is_king

                    # break if king count is at least 2
                    if self.king_count >= 2:
                        break
        else:
            grid_points_to_scan = self.get_grid_points_for_scanning(grid_map, '*')
            deep_scan = self.deep_scan(grid_map, grid_points_to_scan)
            return deep_scan


def go():
    grid_sizes = []
    raw_grid_letters = []
    grid_answers = []
    grids = []  # Grid objects
    current_grid = []

    while True:
        user_input = input()

        if not user_input:
            raw_grid_letters.append(current_grid)
            current_grid = []
            continue
        else:
            # input
            current_grid.append(user_input)

            if len(current_grid) == 8:
                # check if blank board
                is_blank_board = True
                for row in current_grid:
                    if not is_blank_board:
                        break  # break for row in current_grid
                    for char in row:
                        if char != '.':
                            is_blank_board = False
                            break  # break for char in row

                if is_blank_board:
                    break  # stop main while loop

    # create grid objects
    for raw_grid_values in raw_grid_letters:
        grids.append(Grid(raw_grid_values, value=False))

    for i, grid in enumerate(grids):
        grid.scan()
    #     grid.scan(mode='deep')
    #     grid_number = i + 1
    #     grid.print_answer(grid_number, len(grids))
    import pdb; pdb.set_trace()


if __name__ == '__main__':
    go()
