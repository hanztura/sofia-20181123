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

    def __init__(self, raw_grid_letters, answers, size):
        self.raw_grid_letters = raw_grid_letters
        self.answers = answers
        self.cols = size[1]
        self.rows = size[0]
        self.grid = self.generate_grid()
        self.grid_map = self.generate_grid_map()
        self.scanned_level = 0

        self._answers_lowered = []
        self._answers_first_letters = []

        self.final_answers = []

    @property
    def size(self):
        rows = self.rows
        cols = self.cols
        return (rows, cols)

    @property
    def max_col_index(self):
        _max_col_index = self.cols - 1
        return _max_col_index

    @property
    def max_row_index(self):
        _max_row_index = self.rows - 1
        return _max_row_index

    @property
    def answers_lowered(self):
        # return if cached
        if self._answers_lowered:
            return self._answers_lowered

        answers = self.answers.copy()
        answers = [ans.lower() for ans in answers]
        self._answers_lowered = answers  # cache

        return answers

    @property
    def answers_first_letters(self):
        # return if cached
        if self._answers_first_letters:
            return self._answers_first_letters

        answers = self.answers_lowered
        first_letters = [ans[0] for ans in answers]
        first_letters = set(first_letters)
        self._answers_first_letters = first_letters  # cache

        return first_letters

    def print_answers(self):
        final_answers = self.final_answers
        print(final_answers)
        answers, points = [], []
        for ans in final_answers:
            answers.append(ans['answer'])
            points.append(ans['point'])

        answers_given = self.answers_lowered
        answers_given_point = []
        for i in answers_given:
            answers_given_point.append((-1, -1))

        for i, answer in enumerate(answers):
            print(answer)
            answer_point = points[i]
            answer_point_row = answer_point[0]
            answer_point_col = answer_point[1]

            ind = answers_given.index(answer)
            current_point = answers_given_point[ind]
            if current_point == (-1, -1):
                answers_given_point[ind] = answer_point

            current_point_row = current_point[0]
            current_point_col = current_point[1]
            if answer == 'au':
                print(current_point, answer_point, answer)

            row_lesser_equal = answer_point_row <= current_point_row
            col_lesser = answer_point_col < current_point_col

            if row_lesser_equal and col_lesser:
                answers_given_point[ind] = answer_point

        for point in answers_given_point:
            message = '{} {}'.format(point[0] + 1, point[1] + 1)
            print(message)

    def generate_grid_map(self):
        grid = self.grid
        grid_map = []
        for row in grid:
            grid_map_row = []
            for i in row:
                grid_map_row.append(True)

            grid_map.append(grid_map_row)

        return grid_map

    def generate_grid(self):
        raw_grid_letters = self.raw_grid_letters
        grid = []
        for _letters in raw_grid_letters:
            letters = [x for x in _letters]
            grid.append(letters)

        return grid

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

    def get_grid_points_for_scanning(self, grid_map):
        for_scanning = []
        for i, row in enumerate(grid_map):
            for j, should_scan in enumerate(row):
                if should_scan:
                    point = (j, i)  # x, y
                    for_scanning.append(point)

                continue

        return for_scanning

    def deep_scan(self, grid, points_to_scan):
        directions = self.MOVE_CALCULATIONS.keys()
        directions = list(directions)
        valid_points = {}
        answers_lowered = self.answers_lowered
        for point in points_to_scan:
            col_index = point[0]
            row_index = point[1]
            scanned_letters = grid[row_index][col_index]  # string
            scanned_letters = scanned_letters.lower()
            _current_answers = [
                ans for ans in answers_lowered if ans.startswith(scanned_letters)]

            valid_answers = []
            valid_answers_directions = []

            for current_answer in _current_answers:
                length = len(current_answer)
                # steps = length - 1

                # compute grid point to get this answer
                for direction in directions:
                    calculation = self.MOVE_CALCULATIONS[direction]
                    _point = list(point)
                    _point[0] += (length - 1) * calculation[0]
                    _point[1] += (length - 1) * calculation[1]
                    # _point = self.move(direction, point, steps, 'yx')
                    is_valid_next_point = self.is_valid_next_point(_point)
                    if is_valid_next_point:
                        valid_answers.append(current_answer)
                        valid_answers_directions.append(direction)

            if valid_answers:
                valid_points[point] = {
                    'answers': valid_answers,
                    'directions': valid_answers_directions
                }
            else:
                self.grid_map[row_index][col_index] = False

        # deep scan level 2, get full text
        for point in valid_points:
            answers = valid_points[point]['answers']
            directions = valid_points[point]['directions']

            for i, answer in enumerate(answers):
                steps = len(answer)
                steps -= 1
                direction = directions[i]
                point_with_letters = self.move(
                    direction, point, steps, True, 'yx'
                )  # ((y, x), letters)

                # check if valid answer
                letters = point_with_letters[1]
                letters = letters.lower()
                if answer == letters:
                    self.final_answers.append(
                        {
                            'point': point_with_letters[0],
                            'answer': letters,
                            'direction': direction

                        }
                    )

    def scan(self, mode='initial'):
        grid = self.grid
        grid_map = self.grid_map
        if mode == 'initial':
            answers_first_letters = self.answers_first_letters

        if mode == 'initial':
            for i, grid_map_row in enumerate(grid_map):
                for j, should_scan in enumerate(grid_map_row):
                    letter = grid[i][j]
                    letter = letter.lower()
                    valid = letter in answers_first_letters
                    if not valid:
                        grid_map[i][j] = False
        else:
            grid_points_to_scan = self.get_grid_points_for_scanning(grid_map)
            deep_scan = self.deep_scan(grid, grid_points_to_scan)
            return deep_scan


def go():
    test_case = int(input())
    grid_sizes = []
    raw_grid_letters = []
    grid_answers = []
    grids = []  # Grid objects

    # input
    for i in range(test_case):
        input()
        grid_size = input().split()  # [rows, cols]
        grid_size = [int(x) for x in grid_size]
        rows = grid_size[0]
        # cols = grid_size[1]

        _raw_grid_letters = []
        for i in range(rows):
            letters = input()
            _raw_grid_letters.append(letters)

        words_to_search_count = int(input())
        _grid_answers = []
        for i in range(words_to_search_count):
            word = input()
            _grid_answers.append(word)

        grid_sizes.append(grid_size)
        raw_grid_letters.append(_raw_grid_letters)
        grid_answers.append(_grid_answers)

        # create grid objects
        grids.append(Grid(_raw_grid_letters, _grid_answers, grid_size))

    for grid in grids:
        grid.scan()
        grid.scan(mode='deep')
        grid.print_answers()


if __name__ == '__main__':
    go()
