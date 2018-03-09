import tools.defines as td
from tools.functions import print_dict
from dictionary.fill_dictionary import modify_value_in_dict
from dictionary.check_dictionary import get_queries


def solve_query(query, expr_list, dictionary):


    print(expr_list)
    if len(expr_list) == 0:
        print ("\t\tin IF!!!!!!")
        modify_value_in_dict(query, td.v_false, dictionary)
    input()

    for expr in expr_list:
        print("in solve query_list[0] {%s} {%s}" %  (query, expr.line))
        copy_dict = dictionary.copy()
        solution = expr.solver(dictionary, query)
    #    print ("isolution", solution)

        if solution is td.Error:
            print("Error : inconsistency")
            dictionary = copy_dict.copy()
            return None




    print_dict(dictionary)

   # input()
