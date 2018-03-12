def usage():
    """ diplay the expert system program usage """

    print("\t\t  -- EXPERT SYSTEM -- \n\n\tUsage:\t\t./expert_system.py [file_to_test]")
    print("\n\tOptions:\n\t\t-p:\tdisplay plain results without visualisation")
    print("\n\t\t-v:\tdisplay regular visualisation (default)")
    print("\n\t\t-c:\tdisplay colorized visualisation")
    print("\n\t\t-d:\tshow filled dictionary at the end of the program")
    #print("\n\t\t-f:\tproceed to extend resolution: using suppositions to solve the queries")
    print("\n\t\t-h:\tdisplay this help")



def get_first_index(to_find, to_search):

    index = -1

    for i, elt in enumerate(to_search):
        if elt in to_find:
             index = i

    return index


def print_dict(dictionary):

    for elt in sorted(dictionary):
        print("[%s:%s]" % (elt, dictionary[elt]))
