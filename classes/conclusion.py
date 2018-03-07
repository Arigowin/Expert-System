import re

import tools.defines as td
from tools.functions import get_first_index
from handle_expression.create_RPN import get_polish_notation


class Conclusion:
    """

    Variables:
        cc
        rpolish

    Functions:
    """


    def __init__(self, cc, dictionary):
        self.cc = cc
        self.rpolish = get_polish_notation(cc)[::-1]
        self._fill_dictionary(dictionary)


    def solver(self, dictionary):
        """ """

        rpolish_cpy = self.rpolish
        self._recu_fct(dictionary, rpolish_cpy)


    def _recu_fct(self, dictionary, rpolish_cpy):
        """ recursive function to call the correct operator function """

        if get_first_index(td.Symbols[:-1], rpolish_cpy) is not -1:
            rpolish_lst = self._split_rpolish(rpolish_cpy)
        print(rpolish_cpy, rpolish_lst)

        if rpolish_copy[0] is '^':
            self._logic_xor(dictionary, rpolish_lst)

        elif rpolish_copy[0] is '|':
            self._logic_or(dictionary, rpolish_lst)

        elif rpolish_copy[0] is '+':
            self._logic_and(dictionary, rpolish_lst)

        elif rpolish_copy[0] is '!':
            self._logic_not(dictionary, rpolish_lst)

        else:
            check_in_dico(rpolish_cpy)


#
    def _logic_xor(dictionary, rpolish_lst):
        """ """

        val = [-1, -1]
        for i, elt in enumerate(rpolish_lst[1:]):

            if len(elt) > 1:
                val[i] = self._recu_fct(dictionary, elt)

            if elt[0].isupper():
                if dictionary[elt][2] == 1:
                    val[i] = dictionary[elt][0]
                else:
                    dictionary[elt][1] = 2

            if elt[0].isdigit():
                val[i] = int(elt)

        if -1 not in val:
            return op.logic_xor(val)
        else:
            # return error
            print("ERROR")






    def _logic_or(dictionary, rpolish_lst):
        """ """


    def _logic_and(dictionary, rpolish_lst):
        """ """


    def _logic_not(dictionary, rpolish_lst):
        """ """


    def _split_rpolish(self, rpolish_cpy):
        """ """

        if get_first_index(td.Symbols[:-1], rpolish_cpy[1:]) is -1:
            match = re.match("([+|^])(!?[A-Z])(!?[A-Z])", rpolish_cpy)

            if match.lastindex == 3:
                return [match.group(1), match.group(2), match.group(3)]

        if rpolish_cpy[0] is '!' and not rpolish_cpy[1].isupper():
            return [rpolish_cpy[0], rpolish_cpy[1:]]
        rpolish_lst = [rpolish_cpy[0]]
        b = False

        index = -1
        for i, elt in enumerate(rpolish_cpy[1:]):

            print(i, elt)
            if elt in "^|+" and b is True:
                index = i + 1
                break

            elif elt.isupper():
                b = True

        if index is not -1:
            rpolish_lst.extend((rpolish_cpy[1:index], rpolish_cpy[index:]))

        return rpolish_lst


    def _fill_dictionary(self, dictionary):

        for elt in self.rpolish:
            if elt.isupper():
                dictionary[elt][1] = 2


