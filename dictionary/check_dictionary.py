import tools.defines as td


def get_queries(dictionary, query_list = []):
    """ get the list of the fact we need to find the value of """

    print("IN GET QUERIES", query_list)

    for elt in dictionary:
        if dictionary[elt][2] is td.m_default and dictionary[elt][1] is not td.q_unused and elt not in query_list:
            query_list.insert(0, elt)

    if len(query_list) > 1:
        query_list.append(query_list.pop(0))
    print("AFTER POP IN GET QUERIES", query_list)
    return query_list


def get_value_from_dict(fact, dictionary):
    """ get the value of the given fact from dictionary
    and add this fact to custom queries if its value is not determined
    """

    if fact.isdigit():
        return int(fact)

    if not fact.isupper():
        return td.Error

    val = dictionary[fact][0] if dictionary[fact][2] > td.m_default else td.v_indet
    dictionary[fact][1] = td.q_needed if val is td.v_indet and dictionary[fact][1] is not td.q_initial else dictionary[fact][1]

    return val


def fact_to_value(expr, dictionary):
    """ modify 'expr' by getting values from dictionary """

    for i, elt in enumerate(expr):

        if elt.isupper():

            if dictionary[elt][2] > td.m_default and dictionary[elt][0] is not td.v_indet:
                expr[i] = str(dictionary[elt][0])

    return ''.join(expr)
