#!/usr/bin/python3

import tools.defines as td
import tools.functions as tf
from classes.btree import Btree
from tools.functions import print_dict
from input_file.input import main_input


def check_with_curr_value(elt, expr_lst, dic):
    needed_rule = [rule for rule in expr_lst if elt in rule.cc_lst]

    for rule in needed_rule:
        if rule.cdt.solver(dic) is td.v_true:
            if rule.cc.solver(dic, elt, -1) == td.v_true:
                dic[elt][2] = 2


if __name__ == "__main__":

    dictionary, expr_lst = main_input()
    for fact in dictionary:
        if dictionary[fact][1] is not td.q_unused:
            print("\n\nMAIN START ", fact)
            new_tree = Btree(dictionary, expr_lst, fact)
            pouet = new_tree.recu_launcher(dictionary, expr_lst)

    for elt in [fact for fact in dictionary if dictionary[fact][2] == -1]:
        check_with_curr_value(elt, expr_lst, dictionary)

    if td.op_dictionary:
        print_dict(dictionary)

    tf.print_query(dictionary)
