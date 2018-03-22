import os
import re
import sys
import string
import argparse

import tools.functions as tf
import tools.defines as td
from handle_expression.expression import create_rule
from dictionary.fill_dictionary import init_dictionary


def strip_line(line):
    """ """

    if '#' in line:
        line = line[:line.index("#")]

    rule = re.sub(r'\s+', '', line)
    if rule:
        return rule

    return None


def parse(filename, dictionary):
    """ """

    init = ''
    query = ''
    rules = []

    with open(filename, 'r') as content:
        print("**************************************************************")

        for line in content:
            print(line[:-1])
            rule = strip_line(line)

            if rule and rule[0] == '=':
                init += rule[1:]

            elif rule and rule[0] == '?':
                query += rule[1:]

            elif rule:
                rules.extend(create_rule(rule, dictionary))

    dictionary = init_dictionary(init, query, dictionary)

    print("**************************************************************")

    return dictionary, rules


def parse_arg():
    """ """

    parser = argparse.ArgumentParser()

    # Fixed argument
    parser.add_argument("file", type=str,
                        help="input file : it will contain a list of rules, "
                             "then a list of initial facts, "
                             "then a list of queries.")

    # Optional argument
    parser.add_argument("-v", "--visualisation",
                        help="display regular visualisation",
                        action="store_true")
    parser.add_argument("-d", "--dictionary",
                        help="show filled dictionary at the end of the program",
                        action="store_true")
    parser.add_argument("-c", "--color",
                        help="display colorized visualisation",
                        action="store_true")

    args = parser.parse_args()

    td.op_visualisation = args.visualisation
    td.op_dictionary = args.dictionary
    td.op_color = args.color

    if os.path.isfile(args.file):
        print(args.file)
        return args.dictionary, args.visualisation, args.color, args.file

    print("EXPERT SYSTEM - Error: File not found or it's not a file")
    parser.print_help()
    sys.exit()


# def get_file():
#     """ """
#
#     arg = sys.argv
#     nb_arg = len(arg)
#
#     if nb_arg == 1:
#         tf.usage()
#         sys.exit()
#
#     elif nb_arg > 2:
#         tf.usage()
#         sys.exit()
#
#     if not os.path.isfile(arg[1]):
#         tf.usage()
#         sys.exit()
#
#     return arg[1]


def main_input():
    """ """

    # filename = get_file()
    #
    # if not filename:
    #     return None

    arg_d, arg_v, arg_c, filename = parse_arg()

    dictionary = dict((letter, [0, 0, 0]) for letter in string.ascii_uppercase)
    dictionary, rules = parse(filename, dictionary)

    return dictionary, rules
