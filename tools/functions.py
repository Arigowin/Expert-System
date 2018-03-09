
def get_first_index(to_find, to_search):

    index = -1

    for i, elt in enumerate(to_search):
        if elt in to_find:
             index = i

    return index


def print_dict(dictionary):

    for elt in sorted(dictionary):
        print("[%s:%s]" % (elt, dictionary[elt]))
