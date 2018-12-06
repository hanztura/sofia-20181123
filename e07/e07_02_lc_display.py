class LCDisplay(object):
    NUMBER_MATRICES = (
        [
            [' ', '-', ' '],
            ['|', ' ', '|'],
            [' ', ' ', ' '],
            ['|', ' ', '|'],
            [' ', '-', ' '],
        ],  # 0
        [
            [' ', ' ', ' '],
            [' ', ' ', '|'],
            [' ', ' ', ' '],
            [' ', ' ', '|'],
            [' ', ' ', ' '],
        ],  # 1
        [
            [' ', '-', ' '],
            [' ', ' ', '|'],
            [' ', '-', ' '],
            ['|', ' ', ' '],
            [' ', '-', ' '],
        ],  # 2
        [
            [' ', '-', ' '],
            [' ', ' ', '|'],
            [' ', '-', ' '],
            [' ', ' ', '|'],
            [' ', '-', ' '],
        ],  # 3
        [
            [' ', ' ', ' '],
            ['|', ' ', '|'],
            [' ', '-', ' '],
            [' ', ' ', '|'],
            [' ', ' ', ' '],
        ],  # 4
        [
            [' ', '-', ' '],
            ['|', ' ', ' '],
            [' ', '-', ' '],
            [' ', ' ', '|'],
            [' ', '-', ' '],
        ],  # 5
        [
            [' ', '-', ' '],
            ['|', ' ', ' '],
            [' ', '-', ' '],
            ['|', ' ', '|'],
            [' ', '-', ' '],
        ],  # 6,
        [
            [' ', '-', ' '],
            [' ', ' ', '|'],
            [' ', ' ', ' '],
            [' ', ' ', '|'],
            [' ', ' ', ' '],
        ],  # 7
        [
            [' ', '-', ' '],
            ['|', ' ', '|'],
            [' ', '-', ' '],
            ['|', ' ', '|'],
            [' ', '-', ' '],
        ],  # 8
        [
            [' ', '-', ' '],
            ['|', ' ', '|'],
            [' ', '-', ' '],
            [' ', ' ', '|'],
            [' ', '-', ' '],
        ],  # 9
    )

    def __init__(self, numbers, size=1):
        self.numbers = numbers
        self.size = size
        self.print_me()

    def print_number_in_a_matrix(self, number_matrix):
        for row in number_matrix:
            string = ''.join(row)
            print(string)

    def compute_column_and_rows(self, size):
        """
        Computes the column and rows of a number matrix based on a given size.

        Returns a (columns, rows) Tuple.
        """
        columns = size + 2
        rows = (2 * size) + 3
        return (columns, rows)

    def get_mid_index_of_list(self, _list):
        length = len(_list)
        mid = (length + 1) // 2
        has_two_mids = bool((length + 1) % 2)
        mid_index = mid - 1

        if has_two_mids:
            return (mid_index, mid)

        return mid_index

    def scale_a_number_matrix(self, number_matrix, size=1):
        _number_matrix = [x.copy() for x in number_matrix]

        if size < 1:
            size = 1

        columns, rows = self.compute_column_and_rows(size)

        # scale middle value of all rows
        for row in _number_matrix:
            # get middle part of the row
            row[1:-1] *= (columns - 2)

        # scale NOT (first, mid, last) rows
        second_first, second_last = _number_matrix[1], _number_matrix[-2]

        for i in range((rows - 3 - 2) // 2):
            _number_matrix.insert(1, second_first)
            _number_matrix.insert(-1, second_last)

        return _number_matrix

    def get_numbers__matrix(
        self, numbers='default', base_matrix='default', scale_size=1
    ):
        if numbers == 'default':
            numbers = self.numbers

        if base_matrix == 'default':
            base_matrix = tuple(self.NUMBER_MATRICES)

        if scale_size != 1:
            scale_size = self.size

        numbers = str(numbers)
        numbers = [int(x) for x in numbers]
        numbers_matrices = numbers.copy()  # propagate values

        for i, num in enumerate(numbers):
            matrix = list(base_matrix[num])
            _matrix = self.scale_a_number_matrix(matrix, scale_size)
            numbers_matrices[i] = _matrix  # update values

        return numbers_matrices

    def combine_matrices(self, matrices, separator=" "):
        combined_matrix = matrices[0].copy()  # populate values

        for i, matrix in enumerate(matrices):
            for j, row in enumerate(matrix):
                if i <= 0:
                    combined_matrix[j] = []
                else:
                    combined_matrix[j] += [separator]
                combined_matrix[j] += row

        return combined_matrix

    def print_me(self, with_blank_on_end=True):
        numbers_matrices = self.get_numbers__matrix(scale_size=self.size)
        combined_matrix = self.combine_matrices(numbers_matrices)

        self.print_number_in_a_matrix(combined_matrix)
        if with_blank_on_end:
            print()


def go():
    # input
    inputs = []
    while True:
        user_input = input()
        if user_input == '0 0':
            break
        else:
            user_input = user_input.split()
            inputs.append(user_input)

    # output
    for user_input in inputs:
        size = int(user_input[0])
        numbers = int(user_input[1])

        LCDisplay(numbers, size)


# run program through go()
if __name__ == '__main__':
    go()
