#!/usr/bin/python3

import tools.defines as td
from classes.btree import Btree
from tools.functions import print_dict
from input_file.input import main_input


if __name__ == "__main__":

    dictionary, expr_lst = main_input()
    for fact in dictionary:
        if dictionary[fact][1] is not td.q_unused:

            new_tree = Btree(dictionary, expr_lst, fact)
            pouet = new_tree.recu_launcher(dictionary, expr_lst)

    print_dict(dictionary)
