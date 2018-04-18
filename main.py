#!/usr/bin/python3

import tools.defines as td
import tools.functions as tf
from classes.btree import Btree
from tools.functions import print_dict
from input_file.input import main_input


if __name__ == "__main__":

    dictionary, expr_lst = main_input()
    for fact in dictionary:
        if dictionary[fact][1] is not td.q_unused:

            new_tree = Btree(dictionary, expr_lst, fact)
            pouet = new_tree.recu_launcher(dictionary, expr_lst)

    print("`````````````````````` END", [fact for fact in dictionary if dictionary[fact][2] == -1])
    input()
    # if not td.op_dictionary:  # TODO: Remove the NOT because by default do not show dictionary
    #     print_dict(dictionary)
    # for elt in [fact for fact in dictionary if dictionary[fact][2] == -1]:
    #     needed_rule = [rule for rule in expr_lst if elt in rule.cc_lst]
    #     print(" *** END", needed_rule)
    #     for rule in needed_rule:
    #         print("rules to check", rule.expr, rule.cdt.solver(dictionary))
    #         if rule.cdt.solver(dictionary) is td.v_true:
    #             check_with_curr_value() # TODO!!!
    
    if not td.op_dictionary:  # TODO: Remove the NOT because by default do not show dictionary
        print_dict(dictionary)

    tf.print_query(dictionary)
