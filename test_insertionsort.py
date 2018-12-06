# insertion sort
def insertion_sort(A):
    A = A.copy()
    for i, value in enumerate(A):
        # select value to be inserted
        value_to_insert = value
        hole_position = i

        # locate hole position for the element to be inserted
        while (hole_position > 0) and (A[hole_position - 1] > value_to_insert):
            A[hole_position] = A[hole_position - 1]
            hole_position -= 1

        # insert the number at hole position
        A[hole_position] = value_to_insert

    return A


def go():
    test_cases_length = int(input())
    raw_test_cases = []
    test_cases = []

    # collect test cases
    for i in range(test_cases_length):
        test_case = input()
        raw_test_cases.append(test_case)

    # transform raw test cases into list of integers
    for raw in raw_test_cases:
        test_case = raw.split('|')
        test_case = [int(x) for x in test_case]
        test_cases.append(test_case)

    for test_case in test_cases:
        print(insertion_sort(test_case))


if __name__ == '__main__':
    go()
