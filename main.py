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

    if not td.op_dictionary:  # TODO: Remove the NOT because by default do not show dictionary
        print_dict(dictionary)

    tf.print_query(dictionary)
