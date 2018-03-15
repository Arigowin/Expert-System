import tools.defines as td
from tools.functions import print_dict
from solver.solver import solve_query
from dictionary.check_dictionary import get_queries


def check_solved_queries(query_list, dictionary, undef_lst):
    """ loop thought the 'query_list' to check if all the facts in it
    have their value modified
    and remove the facts that have been set from query_list
    """

    boolean = True
    for fact in query_list:

        #print("IN CHECK QUERIES LOOP", fact, dictionary[fact])
        if dictionary[fact][2] is td.m_nset:
            if fact in undef_lst:
                query_list.remove(fact)
                dictionary[fact][2] = td.m_modif
                if query_list:
                    boolean = False
            else:
                undef_lst.append(fact)
                boolean = False

        if dictionary[fact][2] is td.m_default:
            boolean = False

    #print("END CHECK QUERIE", boolean)
    return boolean


# def main_loop(exprs, dictionary):
#     """ """
#
#     query_list = get_queries(dictionary)
#
#     undef_lst = []
#     while check_solved_queries(query_list, dictionary, undef_lst) is False:
#         #print("AFTER CHECK SOLVE", query_list, undef_lst)
#
#         # expr_list = [expr for expr in exprs if query_list and query_list[0] in expr.cc and expr.usable]
#         # expr_list = [expr for expr in exprs if query_list and query_list[0] in [rule.cc.cc for rule in expr.rules] and expr.usable]
#
#         expr_list = []
#
#         for expr in exprs:
#             for rule in expr.rules:
#                 print("rule %s, usable: %s" % (rule, expr.usable))
#                 if query_list and query_list[0] in rule.cc.cc and expr.usable and expr not in expr_list:
#                     expr_list.append(expr)
#
#         print("query: %s expr: {%s}" % (query_list[0], expr_list))
#
#         solve_query(query_list[0], expr_list, dictionary)
#         #print_dict(dictionary)
#
#         query_list = get_queries(dictionary, query_list)
#         input()

def main_loop(exprs, dictionary):
    """ """

    for fact in dictionary:
        recu(fact, exprs, dictionary)


def recu(fact, exprs, dictionary):
    """ """

    if dictionary[fact][1] is not td.q_unused and dictionary[fact][2] <= 0:
        needed_expr = [expr for expr in exprs if fact in expr.cc_lst and
                       fact not in expr.used]

        for expr in needed_expr:
            print("fact:%s, expr:[%s]" % (fact, expr.line))
            # print_dict(dictionary)

            sol = expr.solver(dictionary, fact)

            print("AFTER SOLVED")
            # print_dict(dictionary)

            expr.used.append(fact)

            if sol is td.v_undef:
                for elt in expr.cdt_lst:
                    recu(elt, exprs, dictionary)
                    sol = expr.solver(dictionary, fact)
                    print("IN FOR fact:%s, expr:[%s], sol:%s" % (fact, expr.line, sol))


