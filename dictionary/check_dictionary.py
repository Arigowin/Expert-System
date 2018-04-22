import tools.defines as td


def get_queries(dic, query_list=[]):
    """ get the list of the fact we need to find the value of """

    for elt in dic:
        if (dic[elt][2] is td.m_default
                and dic[elt][1] is not td.q_unused
                and elt not in query_list):
            query_list.insert(0, elt)

    if len(query_list) > 1:
        query_list.append(query_list.pop(0))

    return query_list


def get_value_from_dict(fact, dic, cdt=False):
    """ get the value of the given fact from dictionary
    and add this fact to custom queries if its value is not determined
    """

    if fact.isdigit():
        return int(fact)

    if not fact.isupper():
        return td.Error

    val = (dic[fact][0] if dic[fact][2] is not td.m_default or cdt is True
           else td.v_undef)

    return val


def fact_to_value(expr, dic):
    """ modify 'expr' by getting values from dictionary """

    lst = []
    for i, elt in enumerate(expr):
        if elt[0].isupper():
            lst.append(get_value_from_dict(elt, dic))
        else:
            lst.append(-1)

    return lst
