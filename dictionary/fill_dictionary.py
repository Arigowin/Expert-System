import tools.defines as td
from error.error import error
from tools.custom_return import enable_ret, cust_ret


def init_dictionary(init, query, dictionary):
    """ create an empty dictionary and fill in the initial queries and values"""

    for elt in init:
        dictionary[elt][0] = td.v_true
        dictionary[elt][2] = td.m_initial

    for elt in query:
        dictionary[elt][1] = td.q_initial

    return dictionary


@enable_ret
def modify_value_in_dict(elt, value, dictionary, query, prio=td.m_modif):
    """ check if the given fact has a define value
    and set it to the given value if it is not incoherent
    """

    #print("in MODIF DICT", elt, value, query, prio)
    if not elt.isupper():
        return error(-7)

    if value == dictionary[elt][0]:
        if prio > dictionary[elt][2] and elt is query:
            dictionary[elt][2] = prio
        elif elt is not query and dictionary[elt][2] < prio:
            dictionary[elt][2] = td.m_nset


    else:  # value != dictionary[elt][0]:
        #print("*********************** MODIFY query(%s) elt(%s) val(%s)prio(%s) in dico(%s)prio(%s)" % (query, elt, value, prio, dictionary[elt][0], dictionary[elt][2]))
        if prio < dictionary[elt][2]:
            if dictionary[elt][0] is td.v_undef:

                dictionary[elt][0] = value
                dictionary[elt][2] = prio if elt is query else td.m_nset
            else:
                return error(-4)

        if prio == dictionary[elt][2]:
            if dictionary[elt][0] is td.v_undef:
                dictionary[elt][0] = value
                dictionary[elt][2] = prio if elt is query else td.m_nset

            else:
                dictionary[elt][0] = td.v_bugged
                return error(-5)

        if prio > dictionary[elt][2]:
            ##print(">>>>>>>>>>>>>>>>> tell me here!!!!")

            #ret = True if dictionary[elt][0] is not td.v_undef else False
            ##print("RET ========> (%s)" % ret)
            dictionary[elt][0] = value
            dictionary[elt][2] = prio #if elt is query else td.m_nset
            ##print("HERE??§?§?§?§?§")
            #cust_ret(error(-5)) if ret is True else None

    return None

