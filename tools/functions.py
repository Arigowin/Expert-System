import tools.defines as td


def get_first_index(to_find, to_search, n=1, order=True):
    """ return the index of the first element contains in 'to_find'
    in 'to_search'
    """

    if order is False:
        to_search = to_search[::-1]

    index = -1

    for i, elt in enumerate(to_search):
        if elt in to_find:
            if n == 1:
                index = i
                break
            n -= 1

    return index if order else len(to_search) - index - 1


def print_dict(dictionary):
    """ print the whole dictionary with the values of all possible facts """

    print("\nDictionary : ")

    for elt in sorted(dictionary):
        value = ("True" if dictionary[elt][0] is td.v_true else "False"
                 if dictionary[elt][0] is td.v_false else "Undefined"
                 if dictionary[elt][0] is td.v_undef else "Bugged")
        print("\t%s : %s" % (elt, value))


def print_query(dictionary):
    """ print the facts query """

    print("\nQuery : ")

    for elt in sorted(dictionary):
        if dictionary[elt][1] is td.q_initial:
            value = ("True" if dictionary[elt][0] is td.v_true else "False"
                     if dictionary[elt][0] is td.v_false else "Undefined"
                     if dictionary[elt][0] is td.v_undef else "Bugged")
            print("\t%s : %s" % (elt, value))
