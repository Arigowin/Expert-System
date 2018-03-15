import tools.defines as td
from error.error import error


def init_dictionary(init, query, dictionary):
    """ create an empty dictionary and fill in the initial queries and values"""

    for elt in init:
        dictionary[elt][0] = td.v_true
        dictionary[elt][2] = td.m_initial

    for elt in query:
        dictionary[elt][1] = td.q_initial

    return dictionary


def modify_value_in_dict(elt, value, dictionary, query, symb=td.m_modif):
    """ check if the given fact has a define value
    and set it to the given value if it is not incoherent
    """

    if not elt.isupper():
        print("\t fill value error : -7")
        print("\t fill value", elt, query, value, dictionary[elt])
        return error(-7)

    print("modify_value_in_dict [{%s}{%s}] val: %s symb: %s " % (elt, query, value, symb))
    print(dictionary[elt])

    if value == dictionary[elt][0]:
        if symb > dictionary[elt][2] and elt is query:
            dictionary[elt][2] = symb
        elif elt is not query:
            dictionary[elt][2] = td.m_nset


        print("\t1 - fill value OK", elt, query, value, dictionary[elt])
        return None

    if dictionary[elt][2] > 0 and value != dictionary[elt][0]:
        if symb < dictionary[elt][2] and dictionary[elt][0] is not td.v_undef:
            dictionary[elt][0] = td.v_undef
            print("\t fill value error : -4")
            print("\t fill value ", elt, query, value, dictionary[elt])
            return error(-4)

    dictionary[elt][0] = value
    dictionary[elt][2] = symb if elt is query else td.m_nset

    print("\t fill value OK", elt, query, value, dictionary[elt])
    return None
