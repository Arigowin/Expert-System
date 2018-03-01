#!/usr/bin/python3

import os
import re
import sys
import string

from classes.rule import Rule


def strip_line(line):

    if '#' in line:
        line = line[:line.index("#")]
        #print("stripped line (%s)" % line)

    rule = re.sub(r'\s+', '', line)
    #print("line without whithspaces: (%s)" % rule)

    if rule:
        return rule


def fill_rlt_dict(init, query):

    mydict = dict((letter, [0, 0]) for letter in string.ascii_uppercase)
    print("DICO {%s} init (%s)" % (mydict, init))

    for elt in init:
        mydict[elt][0] = 1
    for elt in query:
        mydict[elt][1] = 1

    print("DICO {%s}" % mydict)

    return mydict



def parse(filename):

    init = ''
    query = ''
    rules = []

    with open(filename, 'r') as content:

        for line in content:
            print("line : (%s)" % line)

            rule = strip_line(line)

            if rule and rule[0] == '=':
                init += rule[1:]
            elif rule and rule[0] == '?':
                query += rule[1:]

            elif rule:
                rules.append(Rule(rule))

        #print("init : {%s} queries : {%s}" % (init, query))
        result = fill_rlt_dict(init, query)

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

    return result, rules



if __name__ == '__main__':

    main_input()
