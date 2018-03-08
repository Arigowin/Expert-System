import re

import tools.defines as td
import handle_expression.operators as op
from tools.functions import get_first_index
from handle_expression.create_RPN import get_polish_notation
from dictionary.check_in_dictionary import get_value_from_dict, fact_to_value, \
                                           modify_value_in_dict


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
        rpolish_cpy = fact_to_value(list(rpolish_cpy), dictionary)
        print("solv2", rpolish_cpy)
        rlt = self._recu_fct(dictionary, rpolish_cpy, td.true)
        print("last rlt : ", rlt)


    def _recu_fct(self, dictionary, rpolish_cpy, wanted):
        """ recursive function to call the correct operator function """

        print("recu_fct", rpolish_cpy)
        if get_first_index(td.Symbols[:-1], rpolish_cpy) is not -1:
            rpolish_lst = self._split_rpolish(rpolish_cpy)
        elif rpolish_cpy[0] is '!':
            rpolish_lst = ['!', rpolish_cpy[1:]]

        print("recu fct after split ", rpolish_cpy, rpolish_lst)

#        if rpolish_cpy[0] is '^':
#            rlt = self._logic_xor(dictionary, rpolish_lst)

        if rpolish_cpy[0] is '|':
            rlt = self._logic_or(dictionary, rpolish_lst, wanted)

        elif rpolish_cpy[0] is '+':
            rlt = self._logic_and(dictionary, rpolish_lst, wanted)

        elif rpolish_cpy[0] is '!':
            rlt = self._logic_not(dictionary, rpolish_lst, wanted)

        else:
            rlt = get_value_from_dict(rpolish_cpy[0], dictionary)

        print("rlt rcu : ", rlt)
        return rlt



#    def _logic_xor(self, dictionary, rpolish_lst):
#        """ """
#
#        val = [-1, -1]
#        print(dictionary)
#        for i, elt in enumerate(rpolish_lst[1:]):
#
#            print("xor for star ", i, elt, val)
#
#            if len(elt) > 1:
#                val[i] = self._recu_fct(dictionary, elt)
#                print("dep : ", val, elt)
#
#            print("xor for 1 ", val, elt)
#            if val[i] is -1:
#                val[i] = get_value_from_dict(elt[0], dictionary)
#
#            print("xor for end", elt, val)
#
#        print("xor after for ", val)
#        if -1 not in val:
#            rlt = op.logic_xor(val)
#            print("rlt xor : ", rlt)
#            return rlt
#        else:
#            # return error
#            print("ERROR")


    def _logic_or(self, dictionary, rpolish_lst, wanted):
        """ """

        print("- LOGIC OR -")
        val = [-1, -1]
        for i, elt in enumerate(rpolish_lst[1:]):
            if len(elt) > 1:
                val[i] = self._recu_fct(dictionary, elt, wanted)
            else:
                val[i] = get_value_from_dict(elt, dictionary)

        print("val in OR after for", val)
        if wanted is td.true:
            print("if wanted true and one val true")
            if td.true in val:
                return td.true

            if val.count(td.false) == 1:
                if val[0] is td.false:
                    modify_value_in_dict(rpolish_lst[2], td.true, dictionary)
                else:
                    modify_value_in_dict(rpolish_lst[1], td.true, dictionary)
                return td.true

            if val.count(td.indet) == 2:
                return td.indet

            if val.count(td.false) == 2:
                print("ERROR")
                return td.Error

        if wanted is td.fale:
            if td.true in val:
                print("ERROR")
                return td.Error

            for elt in rpolish_lst[1:]:
                modify_value_in_dict(elt, td.false, dictionary)

            return td.false



    def _logic_and(self, dictionary, rpolish_lst, wanted):
        """ """

        print("- LOGIC AND -")
        val = [-1, -1]
        for i, elt in enumerate(rpolish_lst[1:]):

            if len(elt) > 1:
                val[i] = self._recu_fct(dictionary, elt, wanted)

            elif elt.isupper():
                modify_value_in_dict(elt, wanted, dictionary)
                val[i] = wanted

            else:
                val[i] = int(elt)

        if td.indet in val:
            # si on revient ici et que c'est indet ca veux dire qu'il faut determiner les valeurs par une autre equation
            return td.indet

        if val.count(wanted) is not 2:
            print("1 ERROR - incoherence")
            return td.Error

        return wanted


    def _logic_not(self, dictionary, rpolish_lst, wanted):
        """ """

        print("- LOGIC NOT -")
        inv_rlt = op.logic_not(wanted)

        if len(rpolish_lst[1]) > 1:
            val = op.logic_not(self._recu_fct(dictionary, rpolish_lst[1], inv_rlt))

        elif rpolish_lst[1].isupper():
            modify_value_in_dict(rpolish_lst[1], inv_rlt, dictionary)
            val = inv_rlt

        else:
            val = op.logic_not(rpolish_lst[1])

        if val is not wanted:
            print("2 ERROR - incoherence", val)
            return td.Error

        return val


    def _split_rpolish(self, rpolish_cpy):
        """ """

        print("in split : ", rpolish_cpy)
        if get_first_index(td.Symbols[:-1], rpolish_cpy[1:]) is -1:
            match = re.match("([+|^])(!?[A-Z0-2])(!?[A-Z0-2])", rpolish_cpy)

            if match.lastindex == 3:
                return [match.group(1), match.group(2), match.group(3)]

        if rpolish_cpy[0] is '!' and not rpolish_cpy[1].isupper():
            return [rpolish_cpy[0], rpolish_cpy[1:]]
        rpolish_lst = [rpolish_cpy[0]]
        b = False

        index = -1
        for i, elt in enumerate(rpolish_cpy[1:]):

#            print(i, elt)
            if elt in "^|+" and b is True:
                index = i + 1
                break

            elif elt.isupper() or elt.isdigit():
                b = True

        if index is not -1:
            rpolish_lst.extend((rpolish_cpy[1:index], rpolish_cpy[index:]))

        return rpolish_lst


    def _fill_dictionary(self, dictionary):

        for elt in self.rpolish:
            if elt.isupper() and dictionary[elt][2] == 0:
                dictionary[elt][1] = 2

