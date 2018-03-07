#!/usr/bin/python3

import os
import re
import sys
import string

from classes.expression import Expression


def strip_line(line):

    if '#' in line:
        line = line[:line.index("#")]
        #print("stripped line (%s)" % line)

    rule = re.sub(r'\s+', '', line)
    #print("line without whithspaces: (%s)" % rule)

    if rule:
        return rule


def parse(filename):

    init = ''
    query = ''
    rules = []

    with open(filename, 'r') as content:

        for line in content:
#            print("line : (%s)" % line)

            rule = strip_line(line)

            if rule and rule[0] == '=':
                init += rule[1:]
            elif rule and rule[0] == '?':
                query += rule[1:]

            elif rule:
                rules.append(Expression(rule))

        #print("init : {%s} queries : {%s}" % (init, query))
        #result = fill_rlt_dict(init, query)
    result = None

    return result, rules



def get_file():

    arg = sys.argv
    print(arg)

    nb_arg = len(arg)

    if nb_arg == 1:
        print('this program need a arg.')
        sys.exit()
    elif nb_arg > 2:
        print('this program only need one arg.')
        sys.exit()

    if not os.path.isfile(arg[1]):
        print('You have to give the path to a file')
        sys.exit()

    return arg[1]



def main_input():

    filename = get_file()

    if not filename:
        return

    result, rules = parse(filename)

    return filename



if __name__ == '__main__':

    main_input()
