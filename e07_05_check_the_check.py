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

        'nw1': (-2, -1),
        'nw2': (-1, -2),
        'ne1': (1, -2),
        'ne2': (2, -1),
        'se1': (2, 1),
        'se2': (1, 2),
        'sw1': (-1, 2),
        'sw2': (-2, 1)
    }

    # based on king's location
    CHECK_CALCULATIONS = {
        'p': {
            'steps': 1,
            'K': ('nw', 'ne'),  # nw and ne of white King
            'k': ('sw', 'se'),  # sw and se of black king
        },
        'r': {
            'steps': 0,
            'K': ('we', 'no', 'ea', 'so'),
            'k': ('we', 'no', 'ea', 'so'),
        },
        'b': {
            'steps': 0,
            'K': ('nw', 'ne', 'se', 'sw'),
            'k': ('nw', 'ne', 'se', 'sw'),
        },
        'q': {
            'steps': 0,
            'K': ('we', 'nw', 'no', 'ne', 'ea', 'se', 'so', 'sw'),
            'k': ('we', 'nw', 'no', 'ne', 'ea', 'se', 'so', 'sw'),
        },
        'k': {
            'steps': 1,
            'K': ('we', 'nw', 'no', 'ne', 'ea', 'se', 'so', 'sw'),
            'k': ('we', 'nw', 'no', 'ne', 'ea', 'se', 'so', 'sw'),
        },
        'n': {
            'steps': 1,
            'K': ('nw1', 'nw2', 'ne1', 'ne2', 'se1', 'se2', 'sw1', 'sw2'),
            'k': ('nw1', 'nw2', 'ne1', 'ne2', 'se1', 'se2', 'sw1', 'sw2'),
        },
    }

    def __init__(self, raw_grid_letters, size=(8, 8), value=True):
        self.raw_grid_letters = raw_grid_letters
        self.cols = size[0]
        self.rows = size[1]
        self.grid = self.generate_grid()
        self.grid_map = self.generate_grid_map(value=value)
        self.king_count = 0
        self.in_check = ''

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

    def get_grid_points_for_scanning(self, grid_map, value_for_scanning=True):
        for_scanning = []
        for i, row in enumerate(grid_map):
            for j, value in enumerate(row):
                if value == value_for_scanning:
                    point = (j, i)  # x, y
                    for_scanning.append(point)

                continue

        return for_scanning

    def get_target_position_value(self, target_position):
        col_index = target_position[0]
        row_index = target_position[1]
        target_position_value = self.grid[row_index][col_index]
        return target_position_value

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

    def deep_scan(self, grid, points_to_scan):
        """
        Points to scan are mine points. Or values that are equal to '*' (without
        the '').
        """
        directions = self.MOVE_CALCULATIONS.keys()
        directions = list(directions)
        neutral_pieces = self.CHECK_CALCULATIONS.keys()
        neutral_pieces = list(neutral_pieces)
        in_check = ''

        # points to scan are white/black points
        for point in points_to_scan:
            if in_check:
                break

            king_col_index = point[0]
            king_row_index = point[1]
            king = self.grid[king_row_index][king_col_index]  # k or K

            for piece in neutral_pieces:
                if in_check:
                    break

                check_calculation = self.CHECK_CALCULATIONS[piece]
                steps = check_calculation['steps']
                check_directions = check_calculation[king]
                possible_check_positions = []
                if king == 'k':
                    target_piece = piece.upper()
                else:
                    target_piece = piece.lower()

                for direction in check_directions:
                    # pieces with moves that only has 1 step
                    # pawn, knight, king
                    if steps == 1:
                        target_position = self.move(direction, point)
                        is_valid = self.is_valid_next_point(target_position)
                        if is_valid:
                            target_position_piece = self.get_target_position_value(target_position)
                            if target_position_piece == target_piece:
                                possible_check_positions.append(target_position)

                    if steps == 0:
                        target_point = tuple(point)
                        while True:
                            target_position = self.move(direction, target_point)
                            is_valid = self.is_valid_next_point(target_position)
                            if is_valid:
                                target_point = target_position
                                target_position_piece = self.get_target_position_value(target_position)
                                if target_position_piece == target_piece:
                                    possible_check_positions.append(target_position)
                                    break
                                elif target_position_piece == '.':
                                    continue
                                else:
                                    break
                            else:
                                break

                    if possible_check_positions:
                        # problem solved
                        if king == 'k':
                            in_check = 'black king'
                        else:
                            in_check = 'white king'

                        break

        if not in_check:
            in_check = 'no king'

        self.in_check = in_check
        return in_check

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
            grid_points_to_scan = self.get_grid_points_for_scanning(grid_map, True)
            deep_scan = self.deep_scan(grid_map, grid_points_to_scan)
            return deep_scan

    def print_answer(self, grid_number):
        in_check = self.in_check
        header = 'Game #{}: {} is in check.'.format(str(grid_number), in_check)
        print(header)


def go():
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
        grid.scan(mode='deep')
        grid_number = i + 1
        grid.print_answer(grid_number)
    # g = grids[0]
    # grid_points = g.get_grid_points_for_scanning(g.grid_map)


if __name__ == '__main__':
    go()
