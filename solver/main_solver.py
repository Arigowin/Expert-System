import tools.defines as td
from classes.btree import Btree
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

    return boolean


def main_loop(expr_lst, dictionary):
    """ """

    for fact in dictionary:
        if dictionary[fact][1] is not td.q_unused and dictionary[fact][2] <= 0:
            new_tree = Btree(dictionary, expr_lst, fact)
            pouet = new_tree.recu_launcher(dictionary, expr_lst)
            print("POUET!!", pouet)
        #recu(fact, expr_lst, dictionary)


def recu(fact, expr_lst, dictionary):
    """ """

    if dictionary[fact][1] is not td.q_unused and dictionary[fact][2] <= 0:
        needed_expr = [expr for expr in expr_lst if fact in expr.cc_lst and
                       fact not in expr.used]

        for expr in needed_expr:

            sol = expr.solver(dictionary, fact)

            expr.used.append(fact)

            if sol is td.v_undef:
                for elt in expr.cdt_lst:
                    recu(elt, expr_lst, dictionary)
                    sol = expr.solver(dictionary, fact)

