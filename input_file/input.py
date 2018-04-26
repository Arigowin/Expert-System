import os
import re
import sys
import string
import argparse

import tools.defines as td
from handle_expression.expression import create_rule
from dictionary.fill_dictionary import init_dictionary


def strip_line(line):
    """ remove all the whitespaces from te input lines """

    if '#' in line:
        line = line[:line.index("#")]

    rule = re.sub(r'\s+', '', line)
    if rule:
        return rule

    return None


def parse(filename, dictionary):
    """ parse the file lines to check the syntax of the file """

    init = ''
    query = ''
    rules = []

    with open(filename, 'r') as content:

        for line in content:
            rule = strip_line(line)

            if rule and rule[0] == '=':
                init += rule[1:]

            elif rule and rule[0] == '?':
                query += rule[1:]

            elif rule:
                rules.extend(create_rule(rule, dictionary))

    dictionary = init_dictionary(init, query, dictionary)

    return dictionary, rules


def parse_arg():
    """ parse all the arguments and check the options """

    parser = argparse.ArgumentParser()

    # Fixed arguments
    parser.add_argument("file", type=str,
                        help="input file : it will contain a list of rules, "
                             "then a list of initial facts, "
                             "then a list of queries.")

    # Optional arguments
    parser.add_argument("-v", "--no_visualisation",
                        help="do not display regular visualisation",
                        action="store_false")
    parser.add_argument("-d", "--dictionary",
                        help="show filled dictionary at the end of the program",
                        action="store_true")
    parser.add_argument("-c", "--no_color",
                        help="do not display colorized visualisation",
                        action="store_false")
    parser.add_argument("-i", "--interactive",
                        help="interactively add initial facts and/or queries",
                        action="store_true")

    args = parser.parse_args()

    td.op_visualisation = args.no_visualisation
    td.op_dictionary = args.dictionary
    td.op_color = args.no_color
    td.op_inter = args.interactive

    if os.path.isfile(args.file):
        return args.file

    print("EXPERT SYSTEM - Error: Filename not valid")
    parser.print_help()
    sys.exit()


def main_input():

    filename = parse_arg()

    dictionary = dict((letter, [0, 0, 0]) for letter in string.ascii_uppercase)
    dictionary, rules = parse(filename, dictionary)

    return dictionary, rules
