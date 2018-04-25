import tools.defines as td
from error.error import error


def init_dictionary(init, query, dic):
    """ create an empty dictionary and fill in the initial queries and values
    """

    for elt in init:
        dic[elt][0] = td.v_true
        dic[elt][2] = td.m_initial

    for elt in query:
        dic[elt][1] = td.q_initial

    return dic


def cdt_set_value(dic, elt, value, prio):
    """ Condition for set value of elt """

    return (
        (
         prio < dic[elt][2]
         and dic[elt][0] is td.v_undef
         and value is not td.v_undef
        )
        or
        (
            prio == dic[elt][2]
            and dic[elt][0] is td.v_undef
            and value is not td.v_undef
        )
        or
        (
            prio > dic[elt][2]
            and
            (
                (
                    value is not td.v_undef
                    and dic[elt][2] > 0
                )
                or dic[elt][2] <= 0
            )
        )
    )


def modify_dict(elts, value, dic, query, prio=td.m_modif):
    """ check if the given fact list has a define value
    and set then to the given value if it is not incoherent
    """

    ret = []
    for elt in elts:
        if dic[elt][2] is td.m_initial:
            continue

        if value is td.v_bugged and dic[elt][2] <= prio:
            dic[elt][0] = value
            dic[elt][2] = prio
            continue

        if value == dic[elt][0]:
            dic[elt][2] = (prio if prio > dic[elt][2] and elt is query
                           else td.m_nset if elt is not query
                           and dic[elt][2] < prio
                           else dic[elt][2])
            continue

        if cdt_set_value(dic, elt, value, prio):
            dic[elt][0] = value
            dic[elt][2] = prio if elt is query else td.m_nset
            continue

        if (prio < dic[elt][2] and dic[elt][0] is not td.v_undef
                and value is not td.v_undef):
            ret.append(error(-4, ": value in dictionary: %d, new value: %d" % (dic[elt][0], value)))
            continue

        if (prio == dic[elt][2] and dic[elt][0] is not td.v_undef
                and value is not td.v_undef):
            dic[elt][0] = td.v_bugged
            dic[elt][2] = prio
            ret.append(error(-5, ": value in dictionary: %d, new value: %d" % (dic[elt][0], value)))

    return None if len(ret) == 0 else min(ret)
