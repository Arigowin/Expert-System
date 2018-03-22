import tools.defines as td


def usage(error_str=None):
    """ display the expert system program usage """

    print("\t\t  -- EXPERT SYSTEM -- \n\n\tUsage:\t\t./expert_system.py [file_to_test]")
    if error_str:
        print("\n\tYou tried to to launch this program, but", str)
    print("\n\tOptions:\n\t\t-p:\tdisplay plain results without visualisation")
    print("\n\t\t-v:\tdisplay regular visualisation (default)")
    print("\n\t\t-c:\tdisplay colorized visualisation")
    print("\n\t\t-d:\tshow filled dictionary at the end of the program")
    #print("\n\t\t-f:\tproceed to extend resolution: using suppositions to solve the queries")
    print("\n\t\t-h:\tdisplay this help")


def get_first_index(to_find, to_search):
    """ return the index of the first element contains in 'to_find'
    in 'to_search'
    """

    index = -1
    for i, elt in enumerate(to_search):
        if elt in to_find:
            index = i

    return index


def print_dict(dictionary):
    """ print the whole dictionary with the values of all possible facts """

    for elt in sorted(dictionary):
        print("[%s:%s]" % (elt, dictionary[elt]))

    # for elt in sorted(dictionary):
    #     value = "True" if dictionary[elt][0] is td.v_true else "False" \
    #                  if dictionary[elt][0] is td.v_false else "Undefined"
    #     print("[%s : %s]" % (elt, value))


def print_query(dictionary):
    """ Print the facts query """

    print("Query : ")
    for elt in sorted(dictionary):
        if dictionary[elt][1] is td.q_initial:
            value = "True" if dictionary[elt][0] is td.v_true else "False" \
                         if dictionary[elt][0] is td.v_false else "Undefined"
            print("\t%s : %s" % (elt, value))
