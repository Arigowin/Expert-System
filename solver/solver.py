import tools.defines as td
from tools.functions import print_dict
from dictionary.fill_dictionary import modify_value_in_dict
from dictionary.check_dictionary import get_queries


def solve_query(query, expr_list, dictionary):

    if len(expr_list) == 0:
        modify_value_in_dict(query, td.v_false, dictionary, query)

    for expr in expr_list:

        copy_dict = dictionary.copy()
        solution = expr.solver(dictionary, query)

        if solution < 0:
            dictionary = copy_dict.copy()

            return modify_value_in_dict(query, td.v_undef, dictionary, query, td.m_initial)

