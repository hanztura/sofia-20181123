def linear_search(list_of_words, word_to_search):
    comparisons = 0
    word_location = -1

    for i, word in enumerate(list_of_words):
        comparisons += 1

        if word == word_to_search:
            word_location = i
            break

    is_found = (word_location >= 0)

    if is_found:
        message = 'found'
    else:
        message = 'not found'

    message = '{} {}'.format(message, comparisons)
    print(message)
    return word_location


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

    for i, value in enumerate(words_to_be_searched):
        linear_search(list_of_words, value)


if __name__ == '__main__':
    go()
