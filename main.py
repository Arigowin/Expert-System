#!/usr/bin/python3

import tools.defines as td
import tools.functions as tf
from classes.btree import Btree
from tools.functions import print_dict
from input_file.input import main_input
from tools.display import display_steps


def check_with_curr_value(elt, expr_lst, dic):
    needed_rule = [rule for rule in expr_lst if elt in rule.cc_lst]

    for rule in needed_rule:
        if rule.cdt.solver(dic) is td.v_true:
            if rule.cc.solver(dic, elt, -1) == td.v_true:
                dic[elt][2] = 2


if __name__ == "__main__":

    dic, expr_lst = main_input()
    facts_true = [fact for fact in dic if dic[fact][2] is td.m_initial]
    display_steps("\nKnown facts: ", facts_true, query='', dic=dic)
    for fact in dic:
        if dic[fact][1] is not td.q_unused:
            new_tree = Btree(dic, expr_lst, fact)
            new_tree.recu_launcher(dic, expr_lst)

    for elt in [fact for fact in dic if dic[fact][2] == -1]:
        check_with_curr_value(elt, expr_lst, dic)

    if td.op_dictionary:
        print_dict(dic)

    tf.print_query(dic)
