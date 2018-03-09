import tools.defines as td


def init_dictionary(init, query, query_val, dictionary):
    """ create an empty dictionary and fill in the initial queries and values"""

    for elt in init:
        dictionary[elt][0] = td.v_true
        dictionary[elt][2] = td.m_initial

    for elt in query:
        dictionary[elt][1] = query_val

    return dictionary


def modify_value_in_dict(elt, value, dictionary, symb=td.m_modif):
    """ check if the given fact has a define value
    and set it to the given value if it is not incoherent
    """

    if not elt.isupper():
        # ERROR pas incoherence
        print("ERROR")
        return td.Error


    if value == dictionary[elt][0]:
        if symb > dictionary[elt][2]:
            dictionary[elt][2] = symb
        return None

    if dictionary[elt][2] is not td.m_default and value != dictionary[elt][0]:
        if symb > dictionary[elt][2] or dictionary[elt][0] is td.v_indet :
            dictionary[elt][0] = value
            dictionary[elt][1] = td.q_unused if dictionary[elt][1] is td.q_needed else dictionary[elt][1]
            dictionary[elt][2] = symb
        return td.Error

    dictionary[elt][0] = value
    dictionary[elt][1] = td.q_unused if dictionary[elt][1] is td.q_needed else dictionary[elt][1]
    dictionary[elt][2] = symb
    return None
