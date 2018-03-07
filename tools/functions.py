
def get_first_index(to_find, to_search):

    index = -1

    for i, elt in enumerate(to_search):
        if elt in to_find:
             index = i

    return index
