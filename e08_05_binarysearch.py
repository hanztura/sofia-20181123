def binary_search(list_of_words, word_to_search):
    A = sorted(list_of_words)
    n = len(A)
    x = word_to_search
    lower_bound = 0
    upper_bound = n - 1
    found = False
    logs = []

    while not found:
        if upper_bound < lower_bound:
            logs.append('not found')
            break

        mid_point = lower_bound + (upper_bound - lower_bound) // 2
        mid_point_value = A[mid_point]
        log = '{} {}'.format(mid_point_value, x)
        logs.append(log)

        if mid_point_value < x:
            lower_bound = mid_point + 1

        if mid_point_value > x:
            upper_bound = mid_point - 1

        if mid_point_value == x:
            logs.append('found')
            found = True

    return('\n'.join(logs))


def go():
    list_of_words = []
    words_to_be_searched = []

    # get list of words
    while True:
        user_input = input()
        if user_input == 'XXXXXX':
            break

        list_of_words.append(user_input)

    # get words to be searched
    while True:
        user_input = input()
        if user_input == 'XXXXXX':
            break

        words_to_be_searched.append(user_input)

    text_to_write = []
    for i, value in enumerate(words_to_be_searched):
        text_to_write.append(binary_search(list_of_words, value))

    with open('listofwords.txt', 'w') as f:
        f.write('\n'.join(text_to_write))


if __name__ == '__main__':
    go()
