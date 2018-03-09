import tools.defines as td
from tools.functions import print_dict
from solver.solver import solve_query
from dictionary.check_dictionary import get_queries


def check_solved_queries(query_list, dictionary):
    """ loop thought the 'query_list' to check if all the facts in it
    have their value modified
    and remove the facts that have been set from query_list
    """

    boolean = True
    for fact in query_list:
 #       print("before remove fact[%s][%s]" % (fact, query_list))
        if dictionary[fact][2] is td.m_default:
            boolean = False
        else:
            query_list.remove(fact)
#        print("after remove fact[%s][%s]" % (fact, query_list))

    return boolean


def main_loop(exprs, dictionary):
    """ """

    print_dict(dictionary)
    query_list = get_queries(dictionary)
    #print_dict(dictionary)

    while check_solved_queries(query_list, dictionary) is False:
        print("in solve main loop", query_list)

        expr_list = [expr for expr in exprs if query_list[0] in expr.cc and expr.usable]
     #   print_dict(dictionary)
        solve_query(query_list[0], expr_list, dictionary)
      #  print_dict(dictionary)

    #    if sorted(query_list) == sorted(get_queries(dictionary, query_list)):
    #        print("BoUCLE INFINIE")
    #        input()
    #      #  return None

        query_list = get_queries(dictionary, query_list)
    print_dict(dictionary)


