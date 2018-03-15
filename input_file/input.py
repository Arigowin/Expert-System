import os
import re
import sys
import string

import tools.defines as td
import tools.functions as tf
from classes.expression import Expression
from dictionary.fill_dictionary import init_dictionary


def strip_line(line):

    if '#' in line:
        line = line[:line.index("#")]

    rule = re.sub(r'\s+', '', line)
    if rule:
        return rule

    return None


def parse(filename, dictionary):

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
                rules.append(Expression(rule, dictionary))

    dictionary = init_dictionary(init, query, dictionary)

    print("**************************************************************")

    return dictionary, rules


def get_file():

    arg = sys.argv
    nb_arg = len(arg)

    if nb_arg == 1:
        tf.usage()
        sys.exit()

    elif nb_arg > 2:
        tf.usage()
        sys.exit()

    if not os.path.isfile(arg[1]):
        tf.usage()
        sys.exit()

    return arg[1]


def main_input():

    filename = get_file()

    if not filename:
        return None

    dictionary = dict((letter, [0, 0, 0]) for letter in string.ascii_uppercase)
    dictionary, rules = parse(filename, dictionary)

    return dictionary, rules
