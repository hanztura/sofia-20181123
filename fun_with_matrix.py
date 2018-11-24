class Matrix(object):
    matrix = []
    OPERATIONS_MAP = {
        'row': 'row_exchange',
        'col': 'col_exchange',
        'inc': 'inc',
        'dec': 'dec',
        'transpose': 'transpose',
    }

    def __init__(self, *args, **kwargs):
        self.matrix = kwargs.get('matrix', [])
        self.N = kwargs.get('N', 0)

    def list_index_exchange(self, a, b, _list):
        """
        Swaps the value of index a and index b of Array _list.

        Returns a modified List.
        """
        a_value = _list[a]
        b_value = _list[b]

        _list[a] = b_value
        _list[b] = a_value

        return _list

    def row_exchange(self, a, b, matrix=[]):
        """
        In this operation, row a is interchanged with row b. Rows are labeled
        from 1 to N , with 1 being the top row and N being the bottom row.

        Returns the modified matrix as a List.
        """

        if not matrix:
            matrix = self.matrix.copy()

        if matrix:
            # transform a and b into matrix index, and get their values
            a -= 1
            b -= 1
            matrix = self.list_index_exchange(a, b, matrix)

            return matrix
        else:
            print('Something went wrong')
            return []

    def col_exchange(self, a, b, matrix=[]):
        """
        In this operation, column a is interchanged with column b. Columns are
        labeled from 1 to N , with 1 being the leftmost column and N being the
        rightmost column.

        Returns the modified matrix as a List.
        """

        if not matrix:
            matrix = self.matrix.copy()

        if matrix:
            # transform a and b into matrix index, and get their values
            a -= 1
            b -= 1

            for i, row in enumerate(matrix):
                matrix[i] = self.list_index_exchange(a, b, row.copy())

            return matrix
        else:
            print('Something went wrong')
            return []

    def inc_or_dec(self, operation='+', increment=1, matrix=[], modulo=10):
        """
        In this operation, every cell value is increased by 1 (modulo 10).
        That is, if after adding 1, a cell value becomes 10 we change it to 0.

        Returns the modified matrix as a List.
        """

        if not matrix:
            matrix = self.matrix

        new_matrix = []

        for row in matrix:
            new_row = []

            for value in row:
                if operation == '-':
                    new_value = (value - increment) % modulo
                else:
                    new_value = (value + increment) % modulo

                new_row.append(new_value)

            new_matrix.append(new_row)

        return new_matrix

    def inc(self):
        return self.inc_or_dec('+')

    def dec(self):
        return self.inc_or_dec('-')

    def transpose(self, matrix=[], N=0):
        """
        In this operation, we simply transpose the matrix. Transposing a matrix
        A, denoted by A T , means turning all the rows of the given matrix into
        columns and vice-versa.
        Example:
        1 2 3
        4 5 6
        7 8 9
        1.1
        after transposing becomes
        1 4 7
        2 5 8
        3 6 9

        Returns the modified matrix as a List.
        """
        if not matrix:
            matrix = self.matrix

        if not N:
            N = self.N

        # set up new matrix with size NxN and propagate with None values
        new_matrix = []
        for i in range(N):
            new_row = [None] * N
            new_matrix.append(new_row)

        # transpose values
        for row_index, row in enumerate(matrix):
            for col_index, value in enumerate(row):
                new_matrix[col_index][row_index] = value

        return new_matrix


# matrix = [
#     [1, 2, 3],
#     [4, 5, 6],
#     [7, 8, 9]
# ]

# matrix = Matrix(matrix=matrix, N=3)
# print(matrix.transpose())

# get user inputs
user_matrixes = []
operations = []
sizes = []
T = int(input())  # test cases
for i in range(T):
    N = int(input())  # size of matrix
    _user_matrix = []
    for j in range(N):
        row = input()  # string of integers
        row = [int(x) for x in row]  # convert each char into list of integers
        _user_matrix.append(row)

    M = int(input())  # number of operations to perform
    _operations = []
    for k in range(M):
        operation = input()
        _operations.append(operation)

    user_matrixes.append(_user_matrix)
    sizes.append(N)
    operations.append(_operations)

# output
for i, user_matrix in enumerate(user_matrixes):
    N = sizes[i]
    matrix = Matrix(matrix=user_matrix, N=N)
    for operation_string in operations[i]:
        operation_data = operation_string.split()
        operation = operation_data[0]
        operations_map = Matrix.OPERATIONS_MAP
        func = operations_map[operation]
        func = getattr(matrix, func)

        if operation == 'row' or operation == 'col':
            a, b = operation_data[1], operation_data[2]
            a, b = int(a), int(b)
            new_matrix = func(a, b)
        else:
            new_matrix = func()

        matrix.matrix = new_matrix

    message = 'Case #{}'.format(i + 1)
    print(message)

    for row in matrix.matrix:
        row_string = [str(x) for x in row]
        print(''.join(row_string))

    print()
