#!/usr/bin/python3

import os
import sys


def check_file_content(filename):

    print("yop in check_file_content")



def get_file():

    arg = sys.argv
    print(arg)

    nb_arg = len(arg)

    if nb_arg == 1:
        print('this program need a arg.')
        return
    elif nb_arg > 2:
        print('this program only need one arg.')
        return

    if not os.path.isfile(arg[1]):
        print('You have to give the path to a file')
        return

    return arg[1]



def main_input():

    filename = get_file()

    if not filename:
        return

    check_file_content(filename)

    return filename



if __name__ == '__main__':

    filename = main_input()

    if filename:
        print(filename)
