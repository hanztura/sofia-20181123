def bubble_sort(A):
    A = A.copy()

    for counter in range(1, len(A)):
        i = 0
        while i < len(A) - 1:
            if A[i] > A[i + 1]:
                A[i], A[i + 1] = A[i + 1], A[i]

            i += 1

        if counter % 4 == 0:
            print(A)

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
        print(bubble_sort(test_case))


if __name__ == '__main__':
    go()
