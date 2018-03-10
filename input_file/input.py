#!/usr/bin/python3

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

        for line in content:
            rule = strip_line(line)

            if rule and rule[0] == '=':
                init += rule[1:]

            elif rule and rule[0] == '?':
                query += rule[1:]

            elif rule:
                rules.append(Expression(rule, dictionary))

    dictionary = init_dictionary(init, query, td.q_initial, dictionary)

    return dictionary, rules


def get_file():

    arg = sys.argv
    print(arg)

    nb_arg = len(arg)

    if nb_arg == 1:
        print('this program need a arg.\n')
        tf.usage()
        sys.exit()
    elif nb_arg > 2:
        print('this program only need one arg.')
        tf.usage()
        sys.exit()

    if not os.path.isfile(arg[1]):
        print('You have to give the path to a file')
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