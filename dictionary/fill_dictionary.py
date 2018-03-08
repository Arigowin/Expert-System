import tools.defines as td


def init_dictionary(init, query):
    """ create an empty dictionary and fill in the inital queries and values"""

    dictionary = dict((letter, [0, 0, 0]) for letter in string.ascii_uppercase)

    for elt in init:
        dictionary[elt][0] = td.true
        dictionary[elt][2] = td.inital

    for elt in query:
        dictionary[elt][1] = td.inital


def modify_value_in_dict(elt, value, dictionary):
    """ check if the given fact has a define value
    and set it to the given value if it is not incoherent
    """

    print("\tin modify dict")
    if dictionary[elt][2] != 0 and value == dictionary[elt][0]:
        return None

    if not elt.isupper() or dictionary[elt][2] != 0:
        # ERROR
        print("ERROR")
        return td.Error

    dictionary[elt][0] = value
    dictionary[elt][1] = 0 if dictionary[elt][1] == 2 else dictionary[elt][1]
    dictionary[elt][2] = 2
    return None
