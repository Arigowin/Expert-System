import tools.defines as td
from tools.functions import print_dict
from solver.solver import solve_query
from dictionary.check_dictionary import get_queries


def check_solved_queries(query_list, dictionary, indet_lst):
    """ loop thought the 'query_list' to check if all the facts in it
    have their value modified
    and remove the facts that have been set from query_list
    """

    boolean = True
    for fact in query_list:

        print("IN CHECK QUERIES LOOP", fact, dictionary[fact])
        if dictionary[fact][2] is td.m_nset:
            if fact in indet_lst:
                query_list.remove(fact)
                dictionary[fact][2] = td.m_modif
                if query_list:
                    boolean = False
            else:
                indet_lst.append(fact)
                boolean = False

        if dictionary[fact][2] is td.m_default:
            boolean = False

    print("END CHECK QUERIE", boolean)
    return boolean


def main_loop(exprs, dictionary):
    """ """

    query_list = get_queries(dictionary)

    indet_lst = []
    while check_solved_queries(query_list, dictionary, indet_lst) is False:
        print("AFTER CHECK SOLVE", query_list, indet_lst)

        expr_list = [expr for expr in exprs if query_list and query_list[0] in expr.cc and expr.usable]

        solve_query(query_list[0], expr_list, dictionary)
        print_dict(dictionary)

        query_list = get_queries(dictionary, query_list)
        input()
