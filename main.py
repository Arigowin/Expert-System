#!/usr/bin/python3

import copy

import tools.defines as td
import tools.functions as tf
from classes.btree import Btree
from tools.functions import print_dict
from input_file.input import main_input
from tools.display import display_steps, display_legend, display_rules
from dictionary.fill_dictionary import init_dictionary


def modif_file(msg):
    while(True):
        new = input(msg)
        if new == "exit" or new == '' or (new.isalpha() and new.isupper()):
            return new
        else:
            print("Fact can only be uppercase letters")


def main_loop(default_dic, default_expr_lst):
    dic = copy.deepcopy(default_dic)
    expr_lst = copy.deepcopy(default_expr_lst)

    facts_true = [fact for fact in dic if dic[fact][2] is td.m_initial]

    display_steps("\nKnown facts: ", facts_true, query='', dic=dic)

    display_rules(expr_lst, dic)

    for fact in dic:
        if dic[fact][1] is not td.q_unused:
            new_tree = Btree(dic, expr_lst, fact)
            new_tree.recu_launcher(dic, expr_lst)

    for elt in [fact for fact in dic if dic[fact][2] == -1]:
        tf.check_with_curr_value(elt, expr_lst, dic)

    if td.op_dictionary:
        print_dict(dic)

    tf.print_query(dic)

    if td.op_inter is False:
        return False

    new_fact = modif_file("\nDo you want to change the value of any initial facts ? [or 'exit'] ")
    if new_fact == "exit":
        return False

    new_query = modif_file("\nDo you want to add queries ? [or 'exit'] ")
    if new_query == "exit":
        return False

    init_dictionary(new_fact, new_query, default_dic)

    return True


if __name__ == "__main__":

    default_dic, default_expr_lst = main_input()

    display_legend()

    while(main_loop(default_dic, default_expr_lst)):
        continue
