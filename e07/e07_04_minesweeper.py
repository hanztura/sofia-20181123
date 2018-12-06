# minesweeper
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

    def __init__(self, raw_grid_letters, size, value=True):
        self.raw_grid_letters = raw_grid_letters
        self.cols = size[0]
        self.rows = size[1]
        self.grid = self.generate_grid()
        self.grid_map = self.generate_grid_map(value=value)

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

    def is_mine(self, col, row):
        value = self.grid_map[row][col]
        is_mine = (value == '*')
        return is_mine

    def is_valid_next_point(self, target_position, _format='xy'):
        cols = self.max_col_index
        rows = self.max_row_index
        if _format == 'xy':
            target_col = target_position[0]
            target_row = target_position[1]
        else:
            target_col = target_position[1]
            target_row = target_position[0]
        col_valid = 0 <= target_col <= cols
        row_valid = 0 <= target_row <= rows

        IS_VALID = col_valid and row_valid
        if IS_VALID:
            # check if not mine
            not_mine = (not self.is_mine(target_col, target_row))
            IS_VALID = not_mine

        return IS_VALID

    def move(self, direction, current_position, steps=1, record_steps=False, _format='xy'):
        """
        Returns the location on the grid if move to a direction.

        Returns a Tuple (x, y) or (col, row)
        """
        calculation = self.MOVE_CALCULATIONS[direction]
        target_position = list(current_position).copy()
        position_log = [list(target_position)]
        for j in range(steps):
            for i, pos in enumerate(target_position):
                target_position[i] += calculation[i]
            position_log.append(target_position.copy())

        if _format == 'yx':
            target_position = (target_position[1], target_position[0])

        if record_steps:
            # get characters
            chars = ''
            for pos in position_log:
                c = pos[0]
                r = pos[1]
                chars += self.grid[r][c]

            return (tuple(target_position), chars)

        return tuple(target_position)

    def get_grid_points_for_scanning(self, grid_map, value_for_scanning=True):
        for_scanning = []
        for i, row in enumerate(grid_map):
            for j, value in enumerate(row):
                if value == value_for_scanning:
                    point = (j, i)  # x, y
                    for_scanning.append(point)

                continue

        return for_scanning

    def deep_scan(self, grid, points_to_scan):
        """
        Points to scan are mine points. Or values that are equal to '*' (without
        the '').
        """
        directions = self.MOVE_CALCULATIONS.keys()
        directions = list(directions)

        for point in points_to_scan:
            col_index = point[0]
            row_index = point[1]

            # get the valid points of all 8 adjacents grid map points and add
            # 1 to its value
            adjacent_points = []
            current_position = (col_index, row_index)
            for direction in directions:
                _adjacent_point = self.move(direction, current_position)
                adjacent_points.append(_adjacent_point)

            # get only valid adjacent points
            valid_adjacent_points = [p for p in adjacent_points if self.is_valid_next_point(p)]

            # increment grid map value of valid points by 1
            for valid_point in valid_adjacent_points:
                col = valid_point[0]
                row = valid_point[1]
                grid[row][col] += 1

    def scan(self, mode='initial'):
        grid = self.grid
        grid_map = self.grid_map

        if mode == 'initial':
            for i, grid_row in enumerate(grid):
                for j, char in enumerate(grid_row):
                    mine_value = '*'
                    mine = (char == mine_value)
                    if mine:
                        grid_map[i][j] = mine_value
        else:
            grid_points_to_scan = self.get_grid_points_for_scanning(grid_map, '*')
            deep_scan = self.deep_scan(grid_map, grid_points_to_scan)
            return deep_scan

    def print_answer(self, grid_number, grids_length):
        grid_map = self.grid_map.copy()
        header = 'Field #{}:'.format(str(grid_number))
        print(header)
        for row in grid_map:
            string_row = [str(char) for char in row]
            string_row = ''.join(string_row)
            print(string_row)
        if grid_number != grids_length:
            print()


def go():
    grid_sizes = []
    raw_grid_letters = []
    grid_answers = []
    grids = []  # Grid objects

    while True:
        # space separated string
        grid_size = input()  # n m
        if grid_size == '0 0':
            break

        grid_size = grid_size.split()  # [rows, cols]
        grid_size = [int(x) for x in grid_size]
        rows = grid_size[0]
        cols = grid_size[1]
        grid_size = (cols, rows)

        # input
        _raw_grid_values = []
        for i in range(rows):
            values = input()  # string. like: *...
            _raw_grid_values.append(values)

        raw_grid_letters.append(_raw_grid_values)
        grid_sizes.append((cols, rows))

        # create grid objects
        grids.append(Grid(_raw_grid_values, grid_size, 0))

    for i, grid in enumerate(grids):
        grid.scan()
        grid.scan(mode='deep')
        grid_number = i + 1
        grid.print_answer(grid_number, len(grids))


if __name__ == '__main__':
    go()
