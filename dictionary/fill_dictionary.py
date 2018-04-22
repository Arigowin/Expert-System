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


def modify_dict(elts, value, dictionary, query, prio=td.m_modif):
    """ check if the given fact list has a define value
    and set then to the given value if it is not incoherent
    """

    ret = []

    for elt in elts:
        print("*********************** MODIFY query(%s) elt(%s) val(%s)prio(%s) in dico(%s)prio(%s)" % (query, elt, value, prio, dictionary[elt][0], dictionary[elt][2]))

        ### TODO: REMOVE WHEN PROJECT DONE
        if not elt.isupper():
            ret.append(error(-7))
            continue

        if value is td.v_bugged and dictionary[elt][2]: # is not td.m_initial:
            dictionary[elt][0] = value
            dictionary[elt][2] = prio
            continue

        if value == dictionary[elt][0]:

            dictionary[elt][2] = (prio if prio > dictionary[elt][2] and elt is query
                                  else td.m_nset if elt is not query
                                                 and dictionary[elt][2] < prio
                                  else dictionary[elt][2])

            continue

        if ((prio < dictionary[elt][2] and dictionary[elt][0] is td.v_undef and value is not td.v_undef)
          or (prio == dictionary[elt][2] and dictionary[elt][0] is td.v_undef and value is not td.v_undef)
          or (prio > dictionary[elt][2] and ((value is not td.v_undef and dictionary[elt][2] > 0)
              or dictionary[elt][2] <= 0))):
            dictionary[elt][0] = value
            dictionary[elt][2] = prio if elt is query else td.m_nset

            continue

        if prio < dictionary[elt][2] and dictionary[elt][0] is not td.v_undef and value is not td.v_undef:
            ret.append(error(-4))
            continue

        if prio == dictionary[elt][2] and dictionary[elt][0] is not td.v_undef and value is not td.v_undef:
            dictionary[elt][0] = td.v_bugged
            dictionary[elt][2] = prio
            ret.append(error(-5))

    return None if len(ret) == 0 else min(ret)
