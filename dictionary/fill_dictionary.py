import tools.defines as td
from error.error import error


def init_dictionary(init, query, dictionary):
    """ create an empty dictionary and fill in the initial queries and values """

    for elt in init:
        dictionary[elt][0] = td.v_true
        dictionary[elt][2] = td.m_initial

    for elt in query:
        dictionary[elt][1] = td.q_initial

    return dictionary


def modify_dict(elt, value, dictionary, query, prio=td.m_modif):
    """ check if the given fact has a define value
    and set it to the given value if it is not incoherent
    """

    ### REMOVE WHEN PROJECT DONE
    if not elt.isupper():
        return error(-7)

    print("*********************** MODIFY query(%s) elt(%s) val(%s)prio(%s)\
          in dico(%s)prio(%s)" % (query, elt, value, prio, dictionary[elt][0],
                                  dictionary[elt][2]))

    if value == dictionary[elt][0]:

        dictionary[elt][2] = (prio if prio > dictionary[elt][2] and elt is query
                              else td.m_nset if elt is not query
                                             and dictionary[elt][2] < prio
                              else dictionary[elt][2])

        return None

    ## if value != dictionary[elt][0]:
    # element values modification in the dictionary
    if ((prio < dictionary[elt][2] and dictionary[elt][0] is td.v_undef)
      or (prio == dictionary[elt][2] and dictionary[elt][0] is td.v_undef)
      or prio > dictionary[elt][2]):

        dictionary[elt][0] = value
        dictionary[elt][2] = prio if elt is query else td.m_nset

        return None

    # error checking and returns
    if prio < dictionary[elt][2] and dictionary[elt][0] is not td.v_undef:
        return error(-4)
    if prio == dictionary[elt][2] and dictionary[elt][0] is not td.v_undef:
        dictionary[elt][0] = td.v_bugged
        return error(-5)

    return None
