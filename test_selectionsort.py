# selection sort
def selection_sort(A):
    A = A.copy()
    array_length = len(A)

    for i in range(array_length - 1):
        current_value = A[i]

        # assume current element is minimum
        index_min = i

        # find the minimum element
        for j, value in enumerate(A[i + 1:]):
            if value < A[index_min]:
                index_min = j + i + 1

        # swap the minimum element with the current element
        if index_min != i:
            A[i] = A[index_min]
            A[index_min] = current_value

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
        print(selection_sort(test_case))


if __name__ == '__main__':
    go()
