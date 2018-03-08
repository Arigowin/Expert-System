def get_queries(query_list, dictionary):
    """ get the list of the fact we need to find the value of """

    for elt in dictionary:
        if elt is not in query_list and dictionary[elt][1]:
            query_list.insert(0, elt)

    return query_list

def check_solved_queries(query_list, dictionary):
    """ loop thought the 'query_list' to check if all the facts in it
    have their value modified
    and remove the facts that have been set from query_list
    """

    boolean = True
    for fact in query_list:
        if dictionary[fact][2] == 0:
            boolean = False
        else:
            query_list.remove(fact)

    return boolean


def main_loop(rules, dictionary):
    """ """

    query_list = get_queries([], dictionary)

    while check_solved_queries(query_list, dictionary) is False:

        get_fact_rule_list()






