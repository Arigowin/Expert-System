import tools.defines as td
from classes.btree import Btree
from tools.functions import print_dict
from solver.solver import solve_query
from dictionary.check_dictionary import get_queries


def main_loop(expr_lst, dictionary):
    """ """

    #print_dict(dictionary)
    for fact in dictionary:
        if dictionary[fact][1] is not td.q_unused:
            print("\n\t\tin main IF", fact)
            new_tree = Btree(dictionary, expr_lst, fact)
            pouet = new_tree.recu_launcher(dictionary, expr_lst)
            ##print("POUET!!", pouet)
        #recu(fact, expr_lst, dictionary)

